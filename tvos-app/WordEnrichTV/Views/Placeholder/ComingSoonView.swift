import SwiftUI

struct ComingSoonView: View {
    let title: String
    let subtitle: String
    let systemImage: String

    var body: some View {
        ZStack {
            AppBackground()
            VStack(spacing: 26) {
                Image(systemName: systemImage)
                    .font(.system(size: 72))
                    .foregroundStyle(AppTheme.gold)
                Text(title)
                    .font(.system(size: 46, weight: .bold, design: .rounded))
                    .foregroundStyle(.white)
                Text(subtitle)
                    .font(.system(size: 24))
                    .foregroundStyle(.white.opacity(0.7))
                    .multilineTextAlignment(.center)
                    .frame(maxWidth: 760)

                GlassCard {
                    Text("COMING SOON")
                        .font(.system(size: 18, weight: .bold))
                        .tracking(2)
                        .foregroundStyle(.white.opacity(0.75))
                        .padding(.horizontal, 26)
                        .padding(.vertical, 12)
                }
            }
            .padding(80)
        }
    }
}
