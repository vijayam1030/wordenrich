import Foundation

@MainActor
final class FlashCardViewModel: ObservableObject {
    static let sessionSize = 20

    @Published private(set) var hasStarted = false
    @Published private(set) var deck: [Word] = []
    @Published private(set) var currentIndex = 0
    @Published var isFlipped = false
    @Published private(set) var knownCount = 0
    @Published private(set) var reviewCount = 0
    @Published private(set) var isSessionComplete = false

    private let store: WordStore

    init(store: WordStore) {
        self.store = store
    }

    var currentCard: Word? {
        deck.indices.contains(currentIndex) ? deck[currentIndex] : nil
    }

    var progressText: String {
        guard !deck.isEmpty else { return "0 of 0" }
        return "\(currentIndex + 1) of \(deck.count)"
    }

    var progressFraction: Double {
        guard !deck.isEmpty else { return 0 }
        return Double(currentIndex) / Double(deck.count)
    }

    func start() {
        let count = min(Self.sessionSize, store.words.count)
        deck = Array(store.words.shuffled().prefix(count))
        currentIndex = 0
        isFlipped = false
        knownCount = 0
        reviewCount = 0
        isSessionComplete = false
        hasStarted = true
    }

    func flip() {
        guard !isFlipped else { return }
        isFlipped = true
    }

    func markKnown() {
        guard isFlipped else { return }
        knownCount += 1
        advance()
    }

    func markNeedsReview() {
        guard isFlipped else { return }
        reviewCount += 1
        advance()
    }

    func returnToStart() {
        hasStarted = false
    }

    private func advance() {
        if currentIndex + 1 >= deck.count {
            isSessionComplete = true
        } else {
            currentIndex += 1
            isFlipped = false
        }
    }
}
