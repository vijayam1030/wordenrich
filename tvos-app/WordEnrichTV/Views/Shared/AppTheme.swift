import SwiftUI

enum AppTheme {
    static let periwinkle = Color(red: 0.40, green: 0.49, blue: 0.92)   // #667eea
    static let indigo = Color(red: 0.30, green: 0.12, blue: 0.59)       // deep indigo
    static let ink = Color(red: 0.06, green: 0.07, blue: 0.11)
    static let card = Color.white.opacity(0.08)
    static let cardBorder = Color.white.opacity(0.14)
    static let success = Color(red: 0.20, green: 0.82, blue: 0.55)
    static let failure = Color(red: 0.98, green: 0.36, blue: 0.42)
    static let gold = Color(red: 1.0, green: 0.84, blue: 0.40)
}

struct AppBackground: View {
    var body: some View {
        ZStack {
            LinearGradient(
                colors: [AppTheme.ink, AppTheme.indigo.opacity(0.9), AppTheme.periwinkle.opacity(0.55)],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            RadialGradient(
                colors: [AppTheme.periwinkle.opacity(0.35), .clear],
                center: .topLeading,
                startRadius: 40,
                endRadius: 900
            )
            RadialGradient(
                colors: [AppTheme.gold.opacity(0.12), .clear],
                center: .bottomTrailing,
                startRadius: 80,
                endRadius: 800
            )
        }
        .ignoresSafeArea()
    }
}

struct GlassCard<Content: View>: View {
    var cornerRadius: CGFloat = 28
    @ViewBuilder var content: Content

    var body: some View {
        content
            .background(
                RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                    .fill(.ultraThinMaterial)
                    .opacity(0.55)
            )
            .background(
                RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                    .fill(AppTheme.card)
            )
            .overlay(
                RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                    .stroke(AppTheme.cardBorder, lineWidth: 1)
            )
            .clipShape(RoundedRectangle(cornerRadius: cornerRadius, style: .continuous))
    }
}
