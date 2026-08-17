import Foundation

@MainActor
final class FillBlankViewModel: ObservableObject {
    @Published private(set) var currentWord: Word?
    @Published private(set) var blankedSentence: String = ""
    @Published private(set) var options: [String] = []
    @Published private(set) var selected: String?
    @Published private(set) var isAnswered = false
    @Published private(set) var hasStarted = false
    @Published var showExplanation = false

    @Published private(set) var correctCount = 0
    @Published private(set) var totalCount = 0
    @Published private(set) var streak = 0
    @Published private(set) var bestStreak = 0

    private var usedWords: Set<String> = []
    private var eligibleWords: [(word: Word, sentence: String)] = []
    private var explanationTask: Task<Void, Never>?
    private let store: WordStore

    init(store: WordStore) {
        self.store = store
    }

    var accuracy: Int {
        totalCount == 0 ? 0 : Int((Double(correctCount) / Double(totalCount) * 100).rounded())
    }

    func start() {
        if eligibleWords.isEmpty {
            eligibleWords = store.words.compactMap { word in
                guard let sentence = Self.blankedSentence(for: word) else { return nil }
                return (word, sentence)
            }
        }
        hasStarted = true
        nextQuestion()
    }

    func nextQuestion() {
        explanationTask?.cancel()
        explanationTask = nil

        guard !eligibleWords.isEmpty else { return }
        if usedWords.count > max(eligibleWords.count - 5, 0) {
            usedWords.removeAll()
        }
        let pool = eligibleWords.filter { !usedWords.contains($0.word.word) }
        guard let entry = (pool.isEmpty ? eligibleWords : pool).randomElement() else { return }
        usedWords.insert(entry.word.word)

        var distractors: Set<String> = []
        var attempts = 0
        while distractors.count < 3 && attempts < 200 {
            attempts += 1
            guard let candidate = eligibleWords.randomElement()?.word.word else { break }
            if candidate.caseInsensitiveCompare(entry.word.word) != .orderedSame {
                distractors.insert(candidate)
            }
        }

        var choices = Array(distractors) + [entry.word.word]
        choices.shuffle()

        currentWord = entry.word
        blankedSentence = entry.sentence
        options = choices
        selected = nil
        isAnswered = false
        showExplanation = false
    }

    func select(_ option: String) {
        guard !isAnswered, let word = currentWord else { return }
        selected = option
        isAnswered = true
        totalCount += 1
        if option.caseInsensitiveCompare(word.word) == .orderedSame {
            correctCount += 1
            streak += 1
            bestStreak = max(bestStreak, streak)
        } else {
            streak = 0
        }

        explanationTask?.cancel()
        explanationTask = Task { [weak self] in
            try? await Task.sleep(nanoseconds: 550_000_000)
            guard !Task.isCancelled else { return }
            self?.showExplanation = true
        }
    }

    func advanceToNext() {
        nextQuestion()
    }

    func state(for option: String) -> OptionState {
        guard isAnswered, let word = currentWord else { return .neutral }
        if option.caseInsensitiveCompare(word.word) == .orderedSame {
            return option == selected ? .correct : .fadedCorrectAnswer
        }
        return option == selected ? .incorrect : .neutral
    }

    var isCorrectSelection: Bool {
        guard let word = currentWord else { return false }
        return selected?.caseInsensitiveCompare(word.word) == .orderedSame
    }

    private static func blankedSentence(for word: Word) -> String? {
        guard let regex = try? NSRegularExpression(
            pattern: "\\b\(NSRegularExpression.escapedPattern(for: word.word))\\b",
            options: .caseInsensitive
        ) else { return nil }

        for sentence in word.sentences {
            let fullRange = NSRange(sentence.startIndex..<sentence.endIndex, in: sentence)
            if let match = regex.firstMatch(in: sentence, range: fullRange) {
                let ns = sentence as NSString
                return ns.replacingCharacters(in: match.range, with: "_____")
            }
        }
        return nil
    }
}
