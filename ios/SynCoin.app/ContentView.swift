import SwiftUI

struct ContentView: View {
    @State private var olona = 100
    @State private var trees = 0
    @State private var computeShared = 0
    @State private var isContributing = false
    
    var body: some View {
        ZStack {
            Color(red: 0.05, green: 0.05, blue: 0.1).ignoresSafeArea()
            
            VStack(spacing: 20) {
                Text("🌱 SynCoin")
                    .font(.system(size: 34, weight: .bold))
                    .foregroundColor(.green)
                
                Text("For the common good")
                    .font(.subheadline)
                    .foregroundColor(.gray)
                
                HStack(spacing: 16) {
                    StatCard(title: "Olona", value: "\(olona)", icon: "🎁", color: .yellow)
                    StatCard(title: "Arbres", value: "\(trees)", icon: "🌳", color: .green)
                }
                
                HStack(spacing: 16) {
                    StatCard(title: "Compute", value: "\(computeShared)", icon: "⚡", color: .blue)
                    StatCard(title: "NFTs", value: "0", icon: "🖼️", color: .purple)
                }
                
                Button(action: {
                    isContributing.toggle()
                    if isContributing {
                        computeShared += 10
                        olona += 1
                    }
                }) {
                    Text(isContributing ? "🟢 Je contribue" : "⚪ Prêter mon compute")
                        .font(.title2.bold())
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(isContributing ? Color.green : Color.gray)
                        .cornerRadius(16)
                }
                .padding(.horizontal)
                
                if olona >= 50 {
                    Button(action: {
                        olona -= 50
                        trees += 1
                    }) {
                        Text("🌳 Planter un arbre (50 Olona)")
                            .font(.title3)
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.green.opacity(0.3))
                            .cornerRadius(16)
                    }
                    .padding(.horizontal)
                }
                
                Spacer()
                
                Text("🔋 Max 10% de ta batterie")
                    .font(.caption)
                    .foregroundColor(.gray)
                Text("🌍 For the common good. Not for profit.")
                    .font(.caption)
                    .foregroundColor(.gray)
            }
            .padding()
        }
    }
}

struct StatCard: View {
    let title: String
    let value: String
    let icon: String
    let color: Color
    
    var body: some View {
        VStack(spacing: 8) {
            Text(icon).font(.title)
            Text(value)
                .font(.system(size: 32, weight: .bold))
                .foregroundColor(color)
            Text(title)
                .font(.caption)
                .foregroundColor(.gray)
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(color.opacity(0.1))
        .cornerRadius(16)
    }
}
