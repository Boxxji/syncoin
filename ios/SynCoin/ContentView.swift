import SwiftUI

struct ContentView: View {
    @State private var olona = 100
    @State private var trees = 0
    @State private var compute = 0
    @State private var nfts = 0
    @State private var isContributing = false
    @State private var selectedTab = 0
    @State private var showAlert = false
    @State private var alertMessage = ""
    
    var body: some View {
        TabView(selection: $selectedTab) {
            homeTab
                .tabItem { Label("Home", systemImage: "house.fill") }
                .tag(0)
            
            rewardsTab
                .tabItem { Label("Rewards", systemImage: "gift.fill") }
                .tag(1)
            
            forestTab
                .tabItem { Label("Green Stats", systemImage: "bolt.fill") }
                .tag(2)
            
            profileTab
                .tabItem { Label("Profile", systemImage: "person.fill") }
                .tag(3)
        }
        .tint(.green)
    }
    
    // MARK: - Home
    var homeTab: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 16) {
                    // Header card
                    VStack(spacing: 8) {
                        Image(systemName: "leaf.fill")
                            .font(.system(size: 48))
                            .foregroundStyle(.green)
                            .symbolEffect(.bounce, value: isContributing)
                        
                        Text("SynCoin")
                            .font(.largeTitle.bold())
                        
                        Text("Monetize idle charging time into decentralized AI compute.")
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                    }
                    .padding(.vertical, 24)
                    
                    // Stats grid
                    LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 12) {
                        StatCard(icon: "gift.fill", value: "\(olona)", label: "Olona Balance", color: .yellow)
                        StatCard(icon: "bolt.fill", value: "\(compute)", label: "Compute Cycles", color: .blue)
                        StatCard(icon: "speedometer", value: "35.2 TOPS", label: "Throughput", color: .green)
                        StatCard(icon: "photo.on.rectangle.fill", value: "\(nfts)", label: "Certificates", color: .purple)
                    }
                    
                    // Contribute button
                    Button(action: toggleContribute) {
                        HStack {
                            Image(systemName: isContributing ? "stop.circle.fill" : "play.circle.fill")
                                .font(.title2)
                            Text(isContributing ? "Stop Inférence" : "Start Green Compute")
                                .font(.title3.weight(.semibold))
                        }
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 16)
                        .background(isContributing ? Color.green : Color(uiColor: .systemGray5))
                        .foregroundColor(isContributing ? .white : .primary)
                        .clipShape(RoundedRectangle(cornerRadius: 14))
                    }
                    
                    // Info
                    HStack {
                        Image(systemName: "bolt.batteryblock.fill")
                            .foregroundStyle(.green)
                        Text("100% Direct Payout")
                            .font(.caption)
                            .foregroundStyle(.secondary)
                        Spacer()
                        Text("Zero Intermediary Fees")
                            .font(.caption)
                            .foregroundStyle(.secondary)
                    }
                    .padding(.horizontal, 4)
                }
                .padding()
            }
            .background(Color(.systemGroupedBackground))
            .navigationTitle("SynCoin")
        }
    }
    
    // MARK: - Rewards
    var rewardsTab: some View {
        NavigationStack {
            List {
                Section("Direct Earnings") {
                    HStack {
                        Image(systemName: "gift.fill")
                            .foregroundStyle(.yellow)
                            .font(.title2)
                        VStack(alignment: .leading) {
                            Text("\(olona) Olona")
                                .font(.title2.weight(.bold))
                            Text("100% direct remuneration for AI inference cycles")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }
                    .padding(.vertical, 4)
                }
                
                Section("Redeem & Payout") {
                    ActionRow(icon: "creditcard.fill", color: .green, title: "Withdraw to Solana Wallet",
                             subtitle: "Instant SOL / USDC transfer", disabled: olona < 50) {
                        plantTree()
                    }
                    
                    ActionRow(icon: "photo.on.rectangle.fill", color: .purple, title: "Export Proof Certificate",
                             subtitle: "25 Olona", disabled: olona < 25) {
                        mintNFT()
                    }
                    
                    ActionRow(icon: "wifi", color: .blue, title: "Global P2P Mesh Access",
                             subtitle: "Zero latency routing", disabled: olona < 10) {
                        showAlert("Global P2P Active")
                    }
                }
            }
            .navigationTitle("Rewards")
        }
    }
    
    // MARK: - Green Stats
    var forestTab: some View {
        NavigationStack {
            List {
                Section("Clean Energy Impact") {
                    HStack {
                        Image(systemName: "sun.max.fill")
                            .foregroundStyle(.orange)
                            .font(.system(size: 48))
                        VStack(alignment: .leading, spacing: 4) {
                            Text("100% Decarbonized")
                                .font(.title2.weight(.bold))
                            Text("Powered by solar surplus & off-peak power")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                        .padding(.leading, 8)
                    }
                    .padding(.vertical, 8)
                }
                
                Section("Metrics") {
                    ImpactRow(label: "Clean Energy Share", value: "100% Solar/Battery", icon: "solar_power", color: .orange)
                    ImpactRow(label: "Inference Latency", value: "< 45ms", icon: "wind", color: .teal)
                    ImpactRow(label: "Host Payout Share", value: "100%", icon: "leaf.fill", color: .green)
                }
            }
            .navigationTitle("Green Stats")
        }
    }
    
    // MARK: - Profile
    var profileTab: some View {
        NavigationStack {
            List {
                Section("Host Node") {
                    HStack {
                        Image(systemName: "person.circle.fill")
                            .font(.system(size: 48))
                            .foregroundStyle(.green)
                        VStack(alignment: .leading) {
                            Text("SynCoin Edge Host")
                                .font(.headline)
                            Text("ID: syncoin-\(UUID().uuidString.prefix(8))")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }
                }
                
                Section("Certificates") {
                    if nfts == 0 {
                        Text("No certificates generated yet")
                            .foregroundStyle(.secondary)
                            .padding(.vertical, 8)
                    } else {
                        ForEach(0..<nfts, id: \.self) { i in
                            Label("Certificate #\(i + 1)", systemImage: "photo.on.rectangle.fill")
                        }
                    }
                }
                
                Section("About") {
                    Label("Version 1.0.0", systemImage: "info.circle")
                    Label("License MIT (100% Free)", systemImage: "doc.text")
                    Label("For Lilo 💜 — For Humanity", systemImage: "heart.fill")
                }
            }
            .navigationTitle("Profile")
        }
    }
    
    // MARK: - Actions
    func toggleContribute() {
        isContributing.toggle()
        if isContributing {
            compute += 10
            olona += 1
            alertMessage = "⚡ Inference cycles submitted!"
            showAlert = true
        }
    }
    
    func plantTree() {
        guard olona >= 50 else { return }
        olona -= 50
        trees += 1
        alertMessage = "🌱 Payout / Certificate processed!"
        showAlert = true
    }
    
    func mintNFT() {
        guard olona >= 25 else { return }
        olona -= 25
        nfts += 1
        alertMessage = "🖼️ Proof-of-compute certificate created!"
        showAlert = true
    }
    
    func showAlert(_ msg: String) {
        alertMessage = msg
        showAlert = true
    }
}

// MARK: - Components
struct StatCard: View {
    let icon: String
    let value: String
    let label: String
    let color: Color
    
    var body: some View {
        VStack(spacing: 8) {
            Image(systemName: icon)
                .font(.title2)
                .foregroundStyle(color)
            Text(value)
                .font(.title.weight(.bold))
            Text(label)
                .font(.caption)
                .foregroundStyle(.secondary)
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 16)
        .background(Color(.systemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}

struct ActionRow: View {
    let icon: String
    let color: Color
    let title: String
    let subtitle: String
    let disabled: Bool
    let action: () -> Void
    
    var body: some View {
        HStack {
            Image(systemName: icon)
                .foregroundStyle(color)
                .font(.title2)
                .frame(width: 32)
            VStack(alignment: .leading) {
                Text(title)
                    .font(.body)
                Text(subtitle)
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
            Spacer()
            Button(action: action) {
                Text("Faire")
                    .font(.callout.weight(.semibold))
                    .padding(.horizontal, 16)
                    .padding(.vertical, 8)
                    .background(disabled ? Color(uiColor: .systemGray5) : color)
                    .foregroundColor(disabled ? .secondary : .white)
                    .clipShape(Capsule())
            }
            .disabled(disabled)
        }
        .padding(.vertical, 4)
    }
}

struct ImpactRow: View {
    let label: String
    let value: String
    let icon: String
    let color: Color
    
    var body: some View {
        HStack {
            Image(systemName: icon)
                .foregroundStyle(color)
                .font(.title3)
            Text(label)
                .font(.body)
            Spacer()
            Text(value)
                .font(.callout.weight(.semibold))
                .foregroundStyle(color)
        }
    }
}

#Preview {
    ContentView()
}
