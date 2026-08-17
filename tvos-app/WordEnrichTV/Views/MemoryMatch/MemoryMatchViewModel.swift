import Foundation

struct MemoryTile: Identifiable {
    enum Kind {
        case word
        case meaning
    }

    let id = UUID()
    let pairID: String
    let display: String
    let kind: Kind
}

@MainActor
final class MemoryMatchViewModel: ObservableObject {
    static let pairCount = 8

    @Published private(set) var tiles: [MemoryTile] = []
    @Published private(set) var faceUpIndices: Set<Int> = []
    @Published private(set) var matchedPairIDs: Set<String> = []
    @Published private(set) var moves = 0
    @Published private(set) var hasStarted = false
    @Published private(set) var isComplete = false
    @Published private(set) var isEvaluating = false
    @Published private(set) var lastMismatchIndices: Set<Int> = []

    private var firstSelectedIndex: Int?
    private var evaluationTask: Task<Void, Never>?
    private let store: WordStore

    init(store: WordStore) {
        self.store = store
    }

    var matchesFound: Int { matchedPairIDs.count }
    var totalPairs: Int { Self.pairCount }

    func start() {
        evaluationTask?.cancel()
        evaluationTask = nil

        let count = min(Self.pairCount, store.words.count)
        let words = store.words.shuffled().prefix(count)

        var newTiles: [MemoryTile] = []
        for word in words {
            newTiles.append(MemoryTile(pairID: word.word, display: word.word.capitalized, kind: .word))
            newTiles.append(MemoryTile(pairID: word.word, display: word.meaning, kind: .meaning))
        }
        tiles = newTiles.shuffled()
        faceUpIndices = []
        matchedPairIDs = []
        lastMismatchIndices = []
        moves = 0
        isComplete = false
        isEvaluating = false
        firstSelectedIndex = nil
        hasStarted = true
    }

    func isFaceUp(_ index: Int) -> Bool {
        faceUpIndices.contains(index) || isMatched(index)
    }

    func isMatched(_ index: Int) -> Bool {
        guard tiles.indices.contains(index) else { return false }
        return matchedPairIDs.contains(tiles[index].pairID)
    }

    func select(_ index: Int) {
        guard tiles.indices.contains(index),
              !isEvaluating,
              !isMatched(index),
              !faceUpIndices.contains(index) else { return }

        lastMismatchIndices = []
        faceUpIndices.insert(index)

        guard let first = firstSelectedIndex else {
            firstSelectedIndex = index
            return
        }

        moves += 1

        if tiles[first].pairID == tiles[index].pairID {
            matchedPairIDs.insert(tiles[index].pairID)
            faceUpIndices.remove(first)
            faceUpIndices.remove(index)
            firstSelectedIndex = nil
            if matchedPairIDs.count == totalPairs {
                isComplete = true
            }
        } else {
            isEvaluating = true
            let pending = [first, index]
            evaluationTask = Task { [weak self] in
                try? await Task.sleep(nanoseconds: 900_000_000)
                guard let self, !Task.isCancelled else { return }
                self.faceUpIndices.subtract(pending)
                self.lastMismatchIndices = []
                self.isEvaluating = false
                self.firstSelectedIndex = nil
            }
            lastMismatchIndices = Set(pending)
        }
    }
}
