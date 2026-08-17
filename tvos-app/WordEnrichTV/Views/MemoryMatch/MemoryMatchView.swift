import SwiftUI

struct MemoryMatchView: View {
    let store: WordStore
    @StateObject private var viewModel: MemoryMatchViewModel
    @Namespace private var namespace

    init(store: WordStore) {
        self.store = store
        _viewModel = StateObject(wrappedValue: MemoryMatchViewModel(store: store))
    }

    var body: some View {
        ZStack {
            AppBackground()

            VStack(spacing: 14) {
                HStack(alignment: .center) {
                    header
                    Spacer()
                    if viewModel.hasStarted && !viewModel.isComplete {
                        statBar
                    }
                }

                Spacer(minLength: 0)

                if !viewModel.hasStarted {
                    startPrompt
                } else if viewModel.isComplete {
                    completeView
                } else {
                    gridView
                }

                Spacer(minLength: 0)
            }
            .padding(.top, 30)
            .padding(.horizontal, 90)
            .padding(.bottom, 30)
        }
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 2) {
            Text("Memory Match")
                .font(.system(size: 16, weight: .semibold, design: .rounded))
                .foregroundStyle(AppTheme.gold)
            Text("Pair each word with its meaning")
                .font(.system(size: 26, weight: .bold, design: .rounded))
                .foregroundStyle(.white)
        }
    }

    private var statBar: some View {
        HStack(spacing: 18) {
            ScoreChip(value: "\(viewModel.matchesFound)/\(viewModel.totalPairs)", label: "Matches", tint: AppTheme.success, compact: true)
            ScoreChip(value: "\(viewModel.moves)", label: "Moves", compact: true)
        }
        .fixedSize()
        .padding(.horizontal, 18)
        .padding(.vertical, 10)
        .background(Capsule().fill(Color.white.opacity(0.08)))
        .overlay(Capsule().stroke(AppTheme.cardBorder, lineWidth: 1))
    }

    private var startPrompt: some View {
        VStack(spacing: 24) {
            Image(systemName: "square.grid.3x3.fill")
                .font(.system(size: 56))
                .foregroundStyle(.white.opacity(0.85))
            Text("Flip tiles to match each word\nwith its meaning")
                .font(.system(size: 30, weight: .semibold, design: .rounded))
                .foregroundStyle(.white)
                .multilineTextAlignment(.center)
            Text("\(MemoryMatchViewModel.pairCount) pairs, shuffled every round")
                .font(.system(size: 19))
                .foregroundStyle(.white.opacity(0.6))

            Button {
                viewModel.start()
            } label: {
                Text("Start")
                    .font(.system(size: 26, weight: .bold, design: .rounded))
                    .padding(.horizontal, 52)
                    .padding(.vertical, 16)
            }
            .buttonStyle(.card)
            .tint(AppTheme.periwinkle)
            .prefersDefaultFocus(true, in: namespace)
        }
        .padding(.top, 30)
    }

    private var gridView: some View {
        LazyVGrid(
            columns: Array(repeating: GridItem(.flexible(), spacing: 18), count: 4),
            spacing: 18
        ) {
            ForEach(Array(viewModel.tiles.enumerated()), id: \.element.id) { index, tile in
                MemoryTileView(
                    tile: tile,
                    isFaceUp: viewModel.isFaceUp(index),
                    isMatched: viewModel.isMatched(index),
                    isMismatch: viewModel.lastMismatchIndices.contains(index)
                ) {
                    viewModel.select(index)
                }
                .frame(height: 150)
                .prefersDefaultFocus(index == 0, in: namespace)
            }
        }
        .frame(maxWidth: 1400)
    }

    private var completeView: some View {
        VStack(spacing: 22) {
            Image(systemName: "star.fill")
                .font(.system(size: 56))
                .foregroundStyle(AppTheme.gold)
            Text("All Matched!")
                .font(.system(size: 34, weight: .bold, design: .rounded))
                .foregroundStyle(.white)
            Text("You solved it in \(viewModel.moves) moves")
                .font(.system(size: 20))
                .foregroundStyle(.white.opacity(0.65))

            Button {
                viewModel.start()
            } label: {
                Text("Play Again")
                    .font(.system(size: 26, weight: .bold, design: .rounded))
                    .padding(.horizontal, 52)
                    .padding(.vertical, 16)
            }
            .buttonStyle(.card)
            .tint(AppTheme.periwinkle)
            .prefersDefaultFocus(true, in: namespace)
        }
    }
}
