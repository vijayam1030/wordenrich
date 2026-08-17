import SwiftUI

struct WordDetailPane: View {
    let word: Word

    var body: some View {
        ScrollView(showsIndicators: false) {
            VStack(alignment: .leading, spacing: 24) {
                Text(word.word.capitalized)
                    .font(.system(size: 48, weight: .heavy, design: .rounded))
                    .foregroundStyle(.white)

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
                if !word.sentences.isEmpty {
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Examples".uppercased())
                            .font(.system(size: 14, weight: .semibold))
                            .tracking(1.1)
                            .foregroundStyle(.white.opacity(0.5))
                        ForEach(word.sentences, id: \.self) { sentence in
                            Text("\u{201C}\(sentence)\u{201D}")
                                .font(.system(size: 20, weight: .regular))
                                .italic()
                                .foregroundStyle(.white.opacity(0.85))
                                .fixedSize(horizontal: false, vertical: true)
                        }
                    }
                }
                if !word.origin.isEmpty {
                    VStack(alignment: .leading, spacing: 6) {
                        Text("Origin".uppercased())
                            .font(.system(size: 14, weight: .semibold))
                            .tracking(1.1)
                            .foregroundStyle(.white.opacity(0.5))
                        Text(word.origin)
                            .font(.system(size: 18))
                            .foregroundStyle(.white.opacity(0.7))
                            .fixedSize(horizontal: false, vertical: true)
                    }
                }
            }
            .padding(36)
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .focusable(false)
        .background(
            RoundedRectangle(cornerRadius: 28, style: .continuous)
                .fill(.ultraThinMaterial)
                .opacity(0.55)
        )
        .background(
            RoundedRectangle(cornerRadius: 28, style: .continuous)
                .fill(AppTheme.card)
        )
        .overlay(
            RoundedRectangle(cornerRadius: 28, style: .continuous)
                .stroke(AppTheme.cardBorder, lineWidth: 1)
        )
        .clipShape(RoundedRectangle(cornerRadius: 28, style: .continuous))
        .id(word.word)
        .transition(.opacity)
        .animation(.easeInOut(duration: 0.2), value: word.word)
    }

    private func labeledChips(title: String, items: [String], tint: Color) -> some View {
        VStack(alignment: .leading, spacing: 10) {
            Text(title.uppercased())
                .font(.system(size: 14, weight: .semibold))
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

struct DictionaryEmptyState: View {
    var body: some View {
        VStack(spacing: 18) {
            Image(systemName: "text.book.closed.fill")
                .font(.system(size: 56))
                .foregroundStyle(.white.opacity(0.5))
            Text("No matching words")
                .font(.system(size: 26, weight: .semibold, design: .rounded))
                .foregroundStyle(.white.opacity(0.8))
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(
            RoundedRectangle(cornerRadius: 28, style: .continuous)
                .fill(AppTheme.card)
        )
        .overlay(
            RoundedRectangle(cornerRadius: 28, style: .continuous)
                .stroke(AppTheme.cardBorder, lineWidth: 1)
        )
    }
}
