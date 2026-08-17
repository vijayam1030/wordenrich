import Foundation

@MainActor
final class SpellItViewModel: ObservableObject {
    static let maxLives = 6

    @Published private(set) var currentWord: Word?
    @Published private(set) var guessedLetters: Set<Character> = []
    @Published private(set) var wrongLetters: [Character] = []
    @Published private(set) var isSolved = false
    @Published private(set) var isFailed = false
    @Published private(set) var hasStarted = false
    @Published var showExplanation = false

    @Published private(set) var solvedCount = 0
    @Published private(set) var attemptedCount = 0

    private var usedWords: Set<String> = []
    private var eligibleWords: [Word] = []
    private var explanationTask: Task<Void, Never>?
    private let store: WordStore

    init(store: WordStore) {
        self.store = store
    }

    var isRoundOver: Bool { isSolved || isFailed }
    var livesRemaining: Int { max(Self.maxLives - wrongLetters.count, 0) }

    var maskedLetters: [Character] {
        guard let word = currentWord else { return [] }
        return word.word.uppercased().map { letter in
            guessedLetters.contains(letter) || isFailed ? letter : "_"
        }
    }

    func start() {
        if eligibleWords.isEmpty {
            eligibleWords = store.words.filter { word in
                !word.word.isEmpty && word.word.allSatisfy { $0.isLetter }
            }
        }
        hasStarted = true
        nextWord()
    }

    func nextWord() {
        explanationTask?.cancel()
        explanationTask = nil

        guard !eligibleWords.isEmpty else { return }
        if usedWords.count > max(eligibleWords.count - 5, 0) {
            usedWords.removeAll()
        }
        let pool = eligibleWords.filter { !usedWords.contains($0.word) }
        guard let word = (pool.isEmpty ? eligibleWords : pool).randomElement() else { return }
        usedWords.insert(word.word)

        currentWord = word
        guessedLetters = []
        wrongLetters = []
        isSolved = false
        isFailed = false
        showExplanation = false
        attemptedCount += 1
    }

    func guess(_ letter: Character) {
        guard !isRoundOver, let word = currentWord, !guessedLetters.contains(letter) else { return }
        guessedLetters.insert(letter)

        if word.word.uppercased().contains(letter) {
            let remainingLetters = Set(word.word.uppercased())
            if remainingLetters.isSubset(of: guessedLetters) {
                isSolved = true
                solvedCount += 1
                scheduleExplanation()
            }
        } else {
            wrongLetters.append(letter)
            if wrongLetters.count >= Self.maxLives {
                isFailed = true
                scheduleExplanation()
            }
        }
    }

    func advanceToNext() {
        nextWord()
    }

    var isCorrectSelection: Bool { isSolved }

    private func scheduleExplanation() {
        explanationTask?.cancel()
        explanationTask = Task { [weak self] in
            try? await Task.sleep(nanoseconds: 550_000_000)
            guard !Task.isCancelled else { return }
            self?.showExplanation = true
        }
    }
}
