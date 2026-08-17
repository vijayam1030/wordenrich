import SwiftUI

struct DictionaryRowButtonStyle: ButtonStyle {
    let isSelected: Bool
    @Environment(\.isFocused) private var isFocused

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.system(size: 24, weight: isFocused ? .bold : .medium, design: .rounded))
            .foregroundStyle(.white)
            .padding(.horizontal, 22)
            .padding(.vertical, 14)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(
                RoundedRectangle(cornerRadius: 16, style: .continuous)
                    .fill(fillColor)
            )
            .overlay(
                RoundedRectangle(cornerRadius: 16, style: .continuous)
                    .stroke(isFocused ? Color.white : Color.clear, lineWidth: 3)
            )
            .scaleEffect(isFocused ? 1.03 : 1.0)
            .shadow(color: .black.opacity(isFocused ? 0.3 : 0), radius: isFocused ? 14 : 0, y: isFocused ? 8 : 0)
            .animation(.spring(response: 0.28, dampingFraction: 0.75), value: isFocused)
    }

    private var fillColor: Color {
        if isFocused { return AppTheme.periwinkle.opacity(0.6) }
        if isSelected { return AppTheme.periwinkle.opacity(0.24) }
        return Color.white.opacity(0.05)
    }
}

struct RailButtonStyle: ButtonStyle {
    @Environment(\.isFocused) private var isFocused

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.system(size: 15, weight: .bold, design: .rounded))
            .foregroundStyle(isFocused ? AppTheme.ink : .white.opacity(0.65))
            .frame(width: 30, height: 22)
            .background(
                Capsule().fill(isFocused ? AppTheme.gold : Color.clear)
            )
            .scaleEffect(isFocused ? 1.25 : 1.0)
            .animation(.spring(response: 0.25, dampingFraction: 0.7), value: isFocused)
    }
}
