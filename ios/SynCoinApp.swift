import SwiftUI
import Foundation
import CryptoKit
import Accelerate

// Base58 Encoder for Solana Address
struct Base58 {
    static let alphabet = [UInt8]("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz".utf8)
    static func encode(_ bytes: [UInt8]) -> String {
        var zeros = 0
        for byte in bytes {
            if byte == 0 { zeros += 1 } else { break }
        }
        var size = (bytes.count - zeros) * 138 / 100 + 1
        var b58 = [UInt8](repeating: 0, count: size)
        var length = 0
        for byte in bytes[zeros...] {
            var carry = UInt32(byte)
            var i = 0
            for j in (0..<b58.count).reversed() {
                if carry == 0 && i >= length { break }
                carry += UInt32(b58[j]) << 8
                b58[j] = UInt8(carry % 58)
                carry /= 58
                i += 1
            }
            length = i
        }
        var i = 0
        while i < b58.count && b58[i] == 0 { i += 1 }
        var str = String(repeating: "1", count: zeros)
        for j in i..<b58.count { str.append(Character(UnicodeScalar(alphabet[Int(b58[j])]))) }
        return str
    }
}

@main
struct SynCoinApp: App {
    var body: some Scene {
        WindowGroup {
            GrokTerminalView()
        }
    }
}

// WebSocket Manager
class NodeConnection: ObservableObject {
    @Published var logs: [String] = [
        "> SYNCOIN OS v0.3.0 INITIALIZED",
        "> ACCELERATE vDSP ENGINE LOADED",
        "> SOLANA DEVNET MODULE LOADED",
    ]
    @Published var isConnected = false
    @Published var isComputing = false
    @Published var solBalance: Double = 0.0
    @Published var solanaAddress: String = ""
    @Published var lastGflops: Double = 0.0
    
    private var webSocketTask: URLSessionWebSocketTask?
    private var computeTimer: Timer?
    private var privateKey: Curve25519.Signing.PrivateKey!
    
    init() {
        setupWallet()
    }
    
    private func setupWallet() {
        if let keyData = UserDefaults.standard.data(forKey: "solana_priv_key") {
            privateKey = try? Curve25519.Signing.PrivateKey(rawRepresentation: keyData)
        }
        if privateKey == nil {
            privateKey = Curve25519.Signing.PrivateKey()
            UserDefaults.standard.set(privateKey.rawRepresentation, forKey: "solana_priv_key")
        }
        
        let pubKeyBytes = [UInt8](privateKey.publicKey.rawRepresentation)
        solanaAddress = Base58.encode(pubKeyBytes)
        addLog("> WALLET LOADED: \(solanaAddress.prefix(6))...\(solanaAddress.suffix(4))")
    }
    
    func addLog(_ msg: String) {
        DispatchQueue.main.async {
            self.logs.append("> \(msg)")
            if self.logs.count > 100 {
                self.logs.removeFirst()
            }
        }
    }
    
    func connect() {
        guard let url = URL(string: "ws://127.0.0.1:8766") else { return }
        addLog("CONNECTING TO SYNCOIN NETWORK [ws://127.0.0.1:8766]")
        
        let session = URLSession(configuration: .default)
        webSocketTask = session.webSocketTask(with: url)
        webSocketTask?.resume()
        
        isConnected = true
        receiveMessage()
        
        // Handshake
        let pingMsg = "{\"action\": \"ping\", \"address\": \"\(solanaAddress)\"}"
        webSocketTask?.send(.string(pingMsg)) { error in
            if let error = error {
                self.addLog("FAILED TO SEND PING: \(error.localizedDescription)")
            }
        }
    }
    
    func disconnect() {
        webSocketTask?.cancel(with: .goingAway, reason: nil)
        isConnected = false
        isComputing = false
        computeTimer?.invalidate()
        addLog("CONNECTION CLOSED BY USER.")
    }
    
    private func receiveMessage() {
        webSocketTask?.receive { [weak self] result in
            guard let self = self else { return }
            
            switch result {
            case .failure(let error):
                DispatchQueue.main.async {
                    self.isConnected = false
                    self.isComputing = false
                    self.computeTimer?.invalidate()
                    self.addLog("CONNECTION ERROR: \(error.localizedDescription)")
                }
            case .success(let message):
                switch message {
                case .string(let text):
                    self.handleJson(text)
                default:
                    break
                }
                if self.isConnected {
                    self.receiveMessage()
                }
            }
        }
    }
    
    private func handleJson(_ text: String) {
        guard let data = text.data(using: .utf8),
              let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else {
            addLog("RECV: \(text)")
            return
        }
        
        if let status = json["status"] as? String {
            if status == "ok", let reward = json["sol"] as? Double, let tx = json["tx"] as? String {
                DispatchQueue.main.async {
                    self.solBalance += reward
                }
                addLog("REWARD: +\(String(format: "%.4f", reward)) SOL")
                addLog("TX: \(tx)")
            } else if status == "pong", let node = json["node"] as? String {
                addLog("CONNECTION ESTABLISHED. NODE_ID: \(node)")
            } else {
                addLog("RECV: \(text)")
            }
        }
    }
    
    private func runBenchmark() -> Double {
        let n = 500 // Matrix size (500x500 is fast but measurable)
        var A = [Float](repeating: 1.0, count: n * n)
        var B = [Float](repeating: 1.0, count: n * n)
        var C = [Float](repeating: 0, count: n * n)
        
        let start = CFAbsoluteTimeGetCurrent()
        cblas_sgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
                    Int32(n), Int32(n), Int32(n),
                    1.0, &A, Int32(n),
                    &B, Int32(n),
                    0.0, &C, Int32(n))
        let end = CFAbsoluteTimeGetCurrent()
        let time = end - start
        
        let ops = 2.0 * pow(Double(n), 3)
        let gigaFlops = (ops / time) / 1_000_000_000.0
        return gigaFlops
    }
    
    func toggleCompute() {
        if !isConnected {
            addLog("ERROR: NOT CONNECTED TO NETWORK")
            return
        }
        
        isComputing.toggle()
        
        if isComputing {
            addLog("INITIATING ACCELERATE NATIVE COMPUTE...")
            runComputeLoop()
        } else {
            addLog("COMPUTE SEQUENCE TERMINATED BY USER.")
        }
    }
    
    private func runComputeLoop() {
        guard isComputing && isConnected else { return }
        
        DispatchQueue.global(qos: .userInitiated).async { [weak self] in
            guard let self = self else { return }
            
            let gflops = self.runBenchmark()
            
            DispatchQueue.main.async {
                guard self.isComputing && self.isConnected else { return }
                
                self.lastGflops = gflops
                let msg = "{\"action\": \"compute\", \"gflops\": \(gflops), \"address\": \"\(self.solanaAddress)\"}"
                
                self.webSocketTask?.send(.string(msg)) { error in
                    if error == nil {
                        self.addLog(String(format: "TX: COMPUTE_PROVED [%.2f GFLOPS]", gflops))
                    }
                }
                
                // Anti-Boucle Morte : Respiration de 3 secondes avant le prochain calcul
                DispatchQueue.main.asyncAfter(deadline: .now() + 3.0) {
                    self.runComputeLoop()
                }
            }
        }
    }
}

// SwiftUI View
struct GrokTerminalView: View {
    @StateObject private var node = NodeConnection()
    
    var body: some View {
        VStack(spacing: 0) {
            // Header
            HStack {
                Text("NET: \(node.isConnected ? "ONLINE" : "OFFLINE")")
                Spacer()
                Text("SOL: \(String(format: "%.4f", node.solBalance))")
                Spacer()
                Text(String(format: "%.1f GFLOPS", node.lastGflops))
            }
            .font(.system(size: 13, weight: .bold, design: .monospaced))
            .foregroundColor(.green)
            .padding()
            .border(Color.green, width: 1)
            
            // Terminal Logs
            ScrollViewReader { proxy in
                ScrollView {
                    VStack(alignment: .leading, spacing: 6) {
                        ForEach(0..<node.logs.count, id: \.self) { index in
                            Text(node.logs[index])
                                .font(.system(size: 13, design: .monospaced))
                                .foregroundColor(.green)
                                .frame(maxWidth: .infinity, alignment: .leading)
                                .id(index)
                        }
                    }
                    .padding()
                }
                .onChange(of: node.logs.count) { _ in
                    withAnimation {
                        proxy.scrollTo(node.logs.count - 1, anchor: .bottom)
                    }
                }
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            
            // Wallet Info
            Text("WALLET: \(node.solanaAddress)")
                .font(.system(size: 10, design: .monospaced))
                .foregroundColor(.green.opacity(0.7))
                .padding(.bottom, 5)
            
            // Controls
            HStack(spacing: 16) {
                Button(action: {
                    if node.isConnected {
                        node.disconnect()
                    } else {
                        node.connect()
                    }
                }) {
                    Text(node.isConnected ? "1. DISCONNECT" : "1. CONNECT_NODE")
                        .font(.system(size: 14, weight: .bold, design: .monospaced))
                        .foregroundColor(node.isConnected ? .black : .green)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(node.isConnected ? Color.green : Color.black)
                        .border(Color.green, width: 1.5)
                }
                
                Button(action: {
                    node.toggleCompute()
                }) {
                    Text(node.isComputing ? "HALT_COMPUTE" : "2. START_COMPUTE")
                        .font(.system(size: 14, weight: .bold, design: .monospaced))
                        .foregroundColor(node.isComputing ? .black : .green)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(node.isComputing ? Color.green : Color.black)
                        .border(Color.green, width: 1.5)
                }
                .disabled(!node.isConnected)
                .opacity(node.isConnected ? 1.0 : 0.5)
            }
            .padding()
        }
        .background(Color.black.edgesIgnoringSafeArea(.all))
    }
}
