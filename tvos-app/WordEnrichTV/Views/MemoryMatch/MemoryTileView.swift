import SwiftUI

struct MemoryTileView: View {
    let tile: MemoryTile
    let isFaceUp: Bool
    let isMatched: Bool
    let isMismatch: Bool
    let onTap: () -> Void

    var body: some View {
        Button(action: onTap) {
            Group {
                if isFaceUp {
                    faceUpContent
                } else {
                    faceDownContent
                }
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .padding(14)
        }
        .buttonStyle(MemoryTileButtonStyle(isMatched: isMatched, isMismatch: isMismatch))
        .disabled(isMatched)
        .animation(.easeInOut(duration: 0.2), value: isFaceUp)
    }

    private var faceDownContent: some View {
        Image(systemName: "questionmark")
            .font(.system(size: 30, weight: .bold))
            .foregroundStyle(.white.opacity(0.7))
    }

    @ViewBuilder
    private var faceUpContent: some View {
        switch tile.kind {
        case .word:
            Text(tile.display)
                .font(.system(size: 24, weight: .heavy, design: .rounded))
                .foregroundStyle(.white)
                .multilineTextAlignment(.center)
                .lineLimit(2)
                .minimumScaleFactor(0.6)
        case .meaning:
            Text(tile.display)
                .font(.system(size: 15, weight: .medium))
                .foregroundStyle(.white.opacity(0.95))
                .multilineTextAlignment(.center)
                .lineLimit(5)
                .minimumScaleFactor(0.7)
        }
    }
}

struct MemoryTileButtonStyle: ButtonStyle {
    let isMatched: Bool
    let isMismatch: Bool
    @Environment(\.isFocused) private var isFocused

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .background(
                RoundedRectangle(cornerRadius: 20, style: .continuous)
                    .fill(fillColor)
            )
            .overlay(
                RoundedRectangle(cornerRadius: 20, style: .continuous)
                    .stroke(borderColor, lineWidth: isFocused ? 5 : 1.5)
            )
            .scaleEffect(isFocused ? 1.04 : 1.0)
            .opacity(isMatched ? 0.55 : 1.0)
            .shadow(color: .black.opacity(isFocused ? 0.3 : 0.12), radius: isFocused ? 18 : 6, y: isFocused ? 10 : 4)
            .animation(.spring(response: 0.3, dampingFraction: 0.72), value: isFocused)
            .animation(.easeInOut(duration: 0.2), value: isMatched)
    }

    private var fillColor: Color {
        if isMatched { return AppTheme.success.opacity(0.3) }
        if isMismatch { return AppTheme.failure.opacity(0.35) }
        return AppTheme.card
    }

    private var borderColor: Color {
        if isMatched { return AppTheme.success }
        if isMismatch { return AppTheme.failure }
        return isFocused ? Color.white : AppTheme.cardBorder
    }
}
