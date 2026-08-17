import SwiftUI

enum LetterState {
    case neutral
    case correct
    case wrong
}

struct LetterButtonStyle: ButtonStyle {
    let state: LetterState
    @Environment(\.isFocused) private var isFocused

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.system(size: 24, weight: .bold, design: .rounded))
            .foregroundStyle(.white)
            .frame(width: 64, height: 64)
            .background(
                RoundedRectangle(cornerRadius: 14, style: .continuous)
                    .fill(fillColor)
            )
            .overlay(
                RoundedRectangle(cornerRadius: 14, style: .continuous)
                    .stroke(isFocused ? Color.white : AppTheme.cardBorder, lineWidth: isFocused ? 4 : 1)
            )
            .scaleEffect(isFocused ? 1.08 : 1.0)
            .opacity(state == .neutral ? 1.0 : 0.55)
            .shadow(color: .black.opacity(isFocused ? 0.3 : 0.1), radius: isFocused ? 16 : 4, y: isFocused ? 8 : 2)
            .animation(.spring(response: 0.28, dampingFraction: 0.72), value: isFocused)
            .animation(.easeInOut(duration: 0.2), value: state)
    }

    private var fillColor: Color {
        switch state {
        case .neutral: return AppTheme.card
        case .correct: return AppTheme.success.opacity(0.7)
        case .wrong: return AppTheme.failure.opacity(0.7)
        }
    }
}
