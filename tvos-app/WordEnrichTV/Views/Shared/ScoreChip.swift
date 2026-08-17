import SwiftUI

struct ScoreChip: View {
    let value: String
    let label: String
    var tint: Color = .white

    var body: some View {
        VStack(spacing: 6) {
            Text(value)
                .font(.system(size: 40, weight: .bold, design: .rounded))
                .foregroundStyle(tint)
                .contentTransition(.numericText())
            Text(label.uppercased())
                .font(.system(size: 16, weight: .semibold))
                .tracking(1.2)
                .foregroundStyle(.white.opacity(0.6))
        }
        .frame(maxWidth: .infinity)
    }
}

struct WordChip: View {
    let text: String
    var tint: Color = AppTheme.periwinkle

    var body: some View {
        Text(text)
            .font(.system(size: 22, weight: .semibold))
            .foregroundStyle(.white)
            .padding(.horizontal, 18)
            .padding(.vertical, 10)
            .background(
                Capsule().fill(tint.opacity(0.35))
            )
            .overlay(
                Capsule().stroke(tint.opacity(0.6), lineWidth: 1)
            )
    }
}
