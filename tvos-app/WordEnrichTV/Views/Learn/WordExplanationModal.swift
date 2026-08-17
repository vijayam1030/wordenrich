import SwiftUI

struct WordExplanationModal: View {
    let word: Word
    let isCorrect: Bool
    let onNext: () -> Void

    @FocusState private var nextButtonFocused: Bool

    var body: some View {
        ZStack {
            Color.black.opacity(0.72)
                .ignoresSafeArea()

            VStack(spacing: 0) {
                header
                    .padding(.horizontal, 44)
                    .padding(.top, 36)
                    .padding(.bottom, 20)

                Divider().overlay(Color.white.opacity(0.12))

                ScrollView(showsIndicators: false) {
                    content
                        .padding(.horizontal, 44)
                        .padding(.vertical, 28)
                }
                .frame(maxHeight: 480)

                Divider().overlay(Color.white.opacity(0.12))

                Button {
                    onNext()
                } label: {
                    Text("Next Word")
                        .font(.system(size: 26, weight: .bold, design: .rounded))
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 6)
                }
                .buttonStyle(.card)
                .tint(AppTheme.periwinkle)
                .focused($nextButtonFocused)
                .padding(.horizontal, 44)
                .padding(.vertical, 28)
            }
            .frame(maxWidth: 1180)
            .background(
                RoundedRectangle(cornerRadius: 32, style: .continuous)
                    .fill(.ultraThinMaterial)
            )
            .background(
                RoundedRectangle(cornerRadius: 32, style: .continuous)
                    .fill(AppTheme.ink.opacity(0.92))
            )
            .overlay(
                RoundedRectangle(cornerRadius: 32, style: .continuous)
                    .stroke(AppTheme.cardBorder, lineWidth: 1)
            )
            .clipShape(RoundedRectangle(cornerRadius: 32, style: .continuous))
            .shadow(color: .black.opacity(0.5), radius: 40, y: 20)
        }
        .transition(.opacity.combined(with: .scale(scale: 0.96)))
        .onAppear {
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.05) {
                nextButtonFocused = true
            }
        }
    }

    private var header: some View {
        HStack(spacing: 16) {
            Image(systemName: isCorrect ? "checkmark.circle.fill" : "xmark.circle.fill")
                .font(.system(size: 36))
                .foregroundStyle(isCorrect ? AppTheme.success : AppTheme.failure)
            VStack(alignment: .leading, spacing: 2) {
                Text(isCorrect ? "Correct!" : "Not quite")
                    .font(.system(size: 22, weight: .semibold, design: .rounded))
                    .foregroundStyle(isCorrect ? AppTheme.success : AppTheme.failure)
                Text(word.word.capitalized)
                    .font(.system(size: 40, weight: .heavy, design: .rounded))
                    .foregroundStyle(.white)
            }
            Spacer()
        }
    }

    private var content: some View {
        VStack(alignment: .leading, spacing: 22) {
            Text(word.meaning)
                .font(.system(size: 24, weight: .medium))
                .foregroundStyle(.white.opacity(0.95))
                .fixedSize(horizontal: false, vertical: true)

            if !word.synonyms.isEmpty {
                labeledChips(title: "Synonyms", items: word.synonyms, tint: AppTheme.success)
            }
            if !word.antonyms.isEmpty {
                labeledChips(title: "Antonyms", items: word.antonyms, tint: AppTheme.failure)
            }
            if let sentence = word.sentences.first {
                VStack(alignment: .leading, spacing: 8) {
                    Text("Example".uppercased())
                        .font(.system(size: 15, weight: .semibold))
                        .tracking(1.1)
                        .foregroundStyle(.white.opacity(0.5))
                    Text("\u{201C}\(sentence)\u{201D}")
                        .font(.system(size: 21, weight: .regular))
                        .italic()
                        .foregroundStyle(.white.opacity(0.85))
                        .fixedSize(horizontal: false, vertical: true)
                }
            }
            if !word.origin.isEmpty {
                VStack(alignment: .leading, spacing: 8) {
                    Text("Origin".uppercased())
                        .font(.system(size: 15, weight: .semibold))
                        .tracking(1.1)
                        .foregroundStyle(.white.opacity(0.5))
                    Text(word.origin)
                        .font(.system(size: 19))
                        .foregroundStyle(.white.opacity(0.7))
                        .fixedSize(horizontal: false, vertical: true)
                }
            }
        }
    }

    private func labeledChips(title: String, items: [String], tint: Color) -> some View {
        VStack(alignment: .leading, spacing: 10) {
            Text(title.uppercased())
                .font(.system(size: 15, weight: .semibold))
                .tracking(1.1)
                .foregroundStyle(.white.opacity(0.5))
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 10) {
                    ForEach(items, id: \.self) { item in
                        WordChip(text: item, tint: tint)
                    }
                }
            }
        }
    }
}
