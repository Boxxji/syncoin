import SwiftUI

@main
struct SynCoinApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

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
                .tabItem { Label("Accueil", systemImage: "house.fill") }
                .tag(0)
            
            rewardsTab
                .tabItem { Label("Récompenses", systemImage: "gift.fill") }
                .tag(1)
            
            forestTab
                .tabItem { Label("Forêt", systemImage: "tree.fill") }
                .tag(2)
            
            profileTab
                .tabItem { Label("Profil", systemImage: "person.fill") }
                .tag(3)
        }
        .tint(.green)
    }
    
    // MARK: - Accueil
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
                        
                        Text("Prête ton téléphone. Reçois des cadeaux.")
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                    }
                    .padding(.vertical, 24)
                    
                    // Stats grid
                    LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 12) {
                        StatCard(icon: "gift.fill", value: "\(olona)", label: "Olona", color: .yellow)
                        StatCard(icon: "tree.fill", value: "\(trees)", label: "Arbres", color: .green)
                        StatCard(icon: "bolt.fill", value: "\(compute)", label: "Compute", color: .blue)
                        StatCard(icon: "photo.on.rectangle.fill", value: "\(nfts)", label: "NFTs", color: .purple)
                    }
                    
                    // Contribute button
                    Button(action: toggleContribute) {
                        HStack {
                            Image(systemName: isContributing ? "stop.circle.fill" : "play.circle.fill")
                                .font(.title2)
                            Text(isContributing ? "Stop" : "Contribuer")
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
                        Image(systemName: "battery.25")
                            .foregroundStyle(.secondary)
                        Text("Max 10% batterie")
                            .font(.caption)
                            .foregroundStyle(.secondary)
                        Spacer()
                        Text("For the common good")
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
    
    // MARK: - Récompenses
    var rewardsTab: some View {
        NavigationStack {
            List {
                Section("Olona") {
                    HStack {
                        Image(systemName: "gift.fill")
                            .foregroundStyle(.yellow)
                            .font(.title2)
                        VStack(alignment: .leading) {
                            Text("\(olona) Olona")
                                .font(.title2.weight(.bold))
                            Text("Gagne des Olona en contribuant du compute")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }
                    .padding(.vertical, 4)
                }
                
                Section("Actions") {
                    ActionRow(icon: "tree.fill", color: .green, title: "Planter un arbre",
                             subtitle: "50 Olona", disabled: olona < 50) {
                        plantTree()
                    }
                    
                    ActionRow(icon: "photo.on.rectangle.fill", color: .purple, title: "Mint un NFT",
                             subtitle: "25 Olona", disabled: olona < 25) {
                        mintNFT()
                    }
                    
                    ActionRow(icon: "wifi", color: .blue, title: "Data gratuit",
                             subtitle: "10 Olona/heure", disabled: olona < 10) {
                        showAlert("Bientôt disponible")
                    }
                }
            }
            .navigationTitle("Récompenses")
        }
    }
    
    // MARK: - Forêt
    var forestTab: some View {
        NavigationStack {
            List {
                Section("Impact") {
                    HStack {
                        Image(systemName: "tree.fill")
                            .foregroundStyle(.green)
                            .font(.system(size: 48))
                        VStack(alignment: .leading, spacing: 4) {
                            Text("\(trees) arbres plantés")
                                .font(.title2.weight(.bold))
                            Text("via notre ASBL partenaire")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                        .padding(.leading, 8)
                    }
                    .padding(.vertical, 8)
                }
                
                if trees > 0 {
                    Section("Statistiques") {
                        ImpactRow(label: "CO₂ absorbé", value: "\(trees * 22) kg/an", icon: "cloud.fill", color: .blue)
                        ImpactRow(label: "Oxygène produit", value: "\(trees * 118) kg/an", icon: "wind", color: .teal)
                        ImpactRow(label: "Biodiversité", value: "\(trees * 10) espèces", icon: "leaf.fill", color: .green)
                    }
                }
            }
            .navigationTitle("Ma Forêt")
        }
    }
    
    // MARK: - Profil
    var profileTab: some View {
        NavigationStack {
            List {
                Section("Portefeuille") {
                    HStack {
                        Image(systemName: "person.circle.fill")
                            .font(.system(size: 48))
                            .foregroundStyle(.green)
                        VStack(alignment: .leading) {
                            Text("SynCoin User")
                                .font(.headline)
                            Text("ID: syncoin-\(UUID().uuidString.prefix(8))")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }
                }
                
                Section("NFTs") {
                    if nfts == 0 {
                        Text("Aucun NFT pour le moment")
                            .foregroundStyle(.secondary)
                            .padding(.vertical, 8)
                    } else {
                        ForEach(0..<nfts, id: \.self) { i in
                            Label("NFT #\(i + 1)", systemImage: "photo.on.rectangle.fill")
                        }
                    }
                }
                
                Section("À propos") {
                    Label("Version 0.1", systemImage: "info.circle")
                    Label("Licence AGPL v3", systemImage: "doc.text")
                    Label("Pour Lilo 💜", systemImage: "heart.fill")
                }
            }
            .navigationTitle("Profil")
        }
    }
    
    // MARK: - Actions
    func toggleContribute() {
        isContributing.toggle()
        if isContributing {
            compute += 10
            olona += 1
            alertMessage = "⚡ Contribution envoyée !"
            showAlert = true
        }
    }
    
    func plantTree() {
        guard olona >= 50 else { return }
        olona -= 50
        trees += 1
        alertMessage = "🌱 Un arbre planté !"
        showAlert = true
    }
    
    func mintNFT() {
        guard olona >= 25 else { return }
        olona -= 25
        nfts += 1
        alertMessage = "🖼️ NFT minté !"
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
