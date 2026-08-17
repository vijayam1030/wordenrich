import Foundation
import SwiftUI

enum OptionState: Equatable {
    case neutral
    case correct
    case incorrect
    case fadedCorrectAnswer
}

@MainActor
final class LearnGameViewModel: ObservableObject {
    @Published private(set) var currentWord: Word?
    @Published private(set) var options: [String] = []
    @Published private(set) var selected: String?
    @Published private(set) var isAnswered = false
    @Published private(set) var hasStarted = false

    @Published private(set) var correctCount = 0
    @Published private(set) var totalCount = 0
    @Published private(set) var streak = 0
    @Published private(set) var bestStreak = 0

    private var usedWords: Set<String> = []
    private let store: WordStore

    init(store: WordStore) {
        self.store = store
    }

    var accuracy: Int {
        totalCount == 0 ? 0 : Int((Double(correctCount) / Double(totalCount) * 100).rounded())
    }

    func start() {
        hasStarted = true
        nextQuestion()
    }

    func nextQuestion() {
        if usedWords.count > max(store.words.count - 5, 0) {
            usedWords.removeAll()
        }
        guard let word = store.randomWord(excluding: usedWords) else { return }
        usedWords.insert(word.word)

        let distractors = store.distractorMeanings(correct: word, count: 3)
        var choices = distractors + [word.meaning]
        choices.shuffle()

        currentWord = word
        options = choices
        selected = nil
        isAnswered = false
    }

    func select(_ option: String) {
        guard !isAnswered, let word = currentWord else { return }
        selected = option
        isAnswered = true
        totalCount += 1
        if option == word.meaning {
            correctCount += 1
            streak += 1
            bestStreak = max(bestStreak, streak)
        } else {
            streak = 0
        }
    }

    func state(for option: String) -> OptionState {
        guard isAnswered, let word = currentWord else { return .neutral }
        if option == word.meaning {
            return option == selected ? .correct : .fadedCorrectAnswer
        }
        return option == selected ? .incorrect : .neutral
    }

    var isCorrectSelection: Bool {
        guard let word = currentWord else { return false }
        return selected == word.meaning
    }
}
