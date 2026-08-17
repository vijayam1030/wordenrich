import SwiftUI

struct FlashCardTile: View {
    let word: Word
    let isFlipped: Bool
    let onTap: () -> Void

    var body: some View {
        Button(action: onTap) {
            ZStack {
                if isFlipped {
                    backContent
                } else {
                    frontContent
                }
            }
            .frame(maxWidth: .infinity)
            .frame(height: 460)
            .padding(36)
        }
        .buttonStyle(FlashCardButtonStyle())
        .disabled(isFlipped)
        .id(word.word)
        .transition(.asymmetric(
            insertion: .opacity.combined(with: .scale(scale: 0.97)),
            removal: .opacity
        ))
        .animation(.easeInOut(duration: 0.25), value: isFlipped)
    }

    private var frontContent: some View {
        VStack(spacing: 22) {
            Spacer(minLength: 0)
            Text(word.word.capitalized)
                .font(.system(size: 64, weight: .heavy, design: .rounded))
                .foregroundStyle(.white)
                .multilineTextAlignment(.center)
            Spacer(minLength: 0)
            Label("Select to reveal", systemImage: "hand.tap.fill")
                .font(.system(size: 18, weight: .semibold))
                .foregroundStyle(.white.opacity(0.55))
        }
    }

    private var backContent: some View {
        VStack(alignment: .leading, spacing: 20) {
            Text(word.word.capitalized)
                .font(.system(size: 34, weight: .heavy, design: .rounded))
                .foregroundStyle(AppTheme.gold)

            Text(word.meaning)
                .font(.system(size: 26, weight: .medium))
                .foregroundStyle(.white.opacity(0.95))
                .lineLimit(3)
                .fixedSize(horizontal: false, vertical: true)

            if !word.synonyms.isEmpty {
                VStack(alignment: .leading, spacing: 10) {
                    Text("Synonyms".uppercased())
                        .font(.system(size: 14, weight: .semibold))
                        .tracking(1.1)
                        .foregroundStyle(.white.opacity(0.5))
                    HStack(spacing: 10) {
                        ForEach(word.synonyms.prefix(4), id: \.self) { item in
                            WordChip(text: item, tint: AppTheme.success)
                        }
                    }
                }
            }

            if let sentence = word.sentences.first {
                VStack(alignment: .leading, spacing: 6) {
                    Text("Example".uppercased())
                        .font(.system(size: 14, weight: .semibold))
                        .tracking(1.1)
                        .foregroundStyle(.white.opacity(0.5))
                    Text("\u{201C}\(sentence)\u{201D}")
                        .font(.system(size: 19, weight: .regular))
                        .italic()
                        .foregroundStyle(.white.opacity(0.8))
                        .lineLimit(2)
                        .fixedSize(horizontal: false, vertical: true)
                }
            }

            Spacer(minLength: 0)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}

struct FlashCardButtonStyle: ButtonStyle {
    @Environment(\.isFocused) private var isFocused

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .background(
                RoundedRectangle(cornerRadius: 32, style: .continuous)
                    .fill(.ultraThinMaterial)
                    .opacity(0.5)
            )
            .background(
                RoundedRectangle(cornerRadius: 32, style: .continuous)
                    .fill(AppTheme.card)
            )
            .overlay(
                RoundedRectangle(cornerRadius: 32, style: .continuous)
                    .stroke(isFocused ? Color.white : AppTheme.cardBorder, lineWidth: isFocused ? 5 : 1)
            )
            .clipShape(RoundedRectangle(cornerRadius: 32, style: .continuous))
            .scaleEffect(isFocused ? 1.02 : 1.0)
            .shadow(color: .black.opacity(isFocused ? 0.35 : 0.15), radius: isFocused ? 30 : 12, y: isFocused ? 16 : 8)
            .animation(.spring(response: 0.32, dampingFraction: 0.72), value: isFocused)
    }
}
