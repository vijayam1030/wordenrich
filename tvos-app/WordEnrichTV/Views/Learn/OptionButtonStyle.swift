import SwiftUI

struct OptionButtonStyle: ButtonStyle {
    let state: OptionState
    @Environment(\.isFocused) private var isFocused

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.system(size: 30, weight: .semibold, design: .rounded))
            .multilineTextAlignment(.leading)
            .lineLimit(3)
            .foregroundStyle(foregroundColor)
            .padding(.horizontal, 28)
            .padding(.vertical, 22)
            .frame(maxWidth: .infinity, minHeight: 130, alignment: .leading)
            .background(
                RoundedRectangle(cornerRadius: 24, style: .continuous)
                    .fill(fillColor)
            )
            .overlay(
                RoundedRectangle(cornerRadius: 24, style: .continuous)
                    .stroke(borderColor, lineWidth: isFocused ? 5 : 1.5)
            )
            .scaleEffect(isFocused ? 1.045 : 1.0)
            .shadow(color: shadowColor, radius: isFocused ? 24 : 8, y: isFocused ? 14 : 6)
            .animation(.spring(response: 0.32, dampingFraction: 0.72), value: isFocused)
            .animation(.easeOut(duration: 0.25), value: state)
    }

    private var fillColor: Color {
        switch state {
        case .neutral: return AppTheme.card
        case .correct: return AppTheme.success.opacity(0.85)
        case .incorrect: return AppTheme.failure.opacity(0.85)
        case .fadedCorrectAnswer: return AppTheme.success.opacity(0.35)
        }
    }

    private var borderColor: Color {
        switch state {
        case .neutral: return isFocused ? .white : AppTheme.cardBorder
        case .correct: return AppTheme.success
        case .incorrect: return AppTheme.failure
        case .fadedCorrectAnswer: return AppTheme.success.opacity(0.7)
        }
    }

    private var foregroundColor: Color {
        .white
    }

    private var shadowColor: Color {
        switch state {
        case .correct: return AppTheme.success.opacity(0.5)
        case .incorrect: return AppTheme.failure.opacity(0.5)
        default: return .black.opacity(isFocused ? 0.35 : 0.18)
        }
    }
}
