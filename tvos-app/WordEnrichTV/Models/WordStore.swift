import Foundation

@MainActor
final class WordStore: ObservableObject {
    @Published private(set) var words: [Word] = []
    @Published private(set) var loadError: String?

    init() {
        load()
    }

    private func load() {
        guard let url = Bundle.main.url(forResource: "words", withExtension: "json") else {
            loadError = "words.json not found in bundle"
            return
        }
        do {
            let data = try Data(contentsOf: url)
            words = try JSONDecoder().decode([Word].self, from: data)
        } catch {
            loadError = error.localizedDescription
        }
    }

    func randomWord(excluding used: Set<String>) -> Word? {
        guard !words.isEmpty else { return nil }
        let pool = words.filter { !used.contains($0.word) }
        return (pool.isEmpty ? words : pool).randomElement()
    }

    /// Returns `count` distinct wrong meanings drawn from other words.
    func distractorMeanings(correct: Word, count: Int) -> [String] {
        guard words.count > count else { return [] }
        var usedMeanings: Set<String> = [correct.meaning]
        var result: [String] = []
        var attempts = 0
        while result.count < count && attempts < 300 {
            attempts += 1
            guard let candidate = words.randomElement() else { break }
            if !usedMeanings.contains(candidate.meaning) {
                usedMeanings.insert(candidate.meaning)
                result.append(candidate.meaning)
            }
        }
        return result
    }
}
