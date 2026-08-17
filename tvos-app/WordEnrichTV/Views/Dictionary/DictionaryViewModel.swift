import Foundation

struct WordSection: Identifiable {
    let letter: String
    let words: [Word]
    var id: String { letter }
}

@MainActor
final class DictionaryViewModel: ObservableObject {
    @Published var searchText: String = ""
    @Published var selectedWord: Word?

    let sortedWords: [Word]

    init(store: WordStore) {
        sortedWords = store.words.sorted { $0.word.localizedCaseInsensitiveCompare($1.word) == .orderedAscending }
        selectedWord = sortedWords.first
    }

    var filteredWords: [Word] {
        let trimmed = searchText.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else { return sortedWords }
        return sortedWords.filter { $0.word.localizedCaseInsensitiveContains(trimmed) }
    }

    var sections: [WordSection] {
        let grouped = Dictionary(grouping: filteredWords) { word -> String in
            guard let first = word.word.first, first.isLetter else { return "#" }
            return String(first).uppercased()
        }
        return grouped.keys.sorted().map { WordSection(letter: $0, words: grouped[$0] ?? []) }
    }

    var availableLetters: [String] {
        sections.map(\.letter)
    }

    func select(_ word: Word) {
        selectedWord = word
    }
}
