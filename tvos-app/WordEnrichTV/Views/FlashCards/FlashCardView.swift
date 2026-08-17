import SwiftUI

struct FlashCardView: View {
    let store: WordStore
    @StateObject private var viewModel: FlashCardViewModel
    @Namespace private var namespace

    @FocusState private var cardFocused: Bool
    @FocusState private var reviewButtonFocused: Bool

    init(store: WordStore) {
        self.store = store
        _viewModel = StateObject(wrappedValue: FlashCardViewModel(store: store))
    }

    var body: some View {
        ZStack {
            AppBackground()

            VStack(spacing: 14) {
                HStack(alignment: .center) {
                    header
                    Spacer()
                    if viewModel.hasStarted && !viewModel.isSessionComplete {
                        statBar
                    }
                }

                Spacer(minLength: 0)

                if !viewModel.hasStarted {
                    startPrompt
                } else if viewModel.isSessionComplete {
                    summaryView
                } else {
                    sessionView
                }

                Spacer(minLength: 0)
            }
            .padding(.top, 30)
            .padding(.horizontal, 90)
            .padding(.bottom, 30)
        }
        .onChange(of: viewModel.isFlipped) { _, flipped in
            if flipped {
                DispatchQueue.main.asyncAfter(deadline: .now() + 0.05) {
                    reviewButtonFocused = true
                }
            } else {
                DispatchQueue.main.asyncAfter(deadline: .now() + 0.05) {
                    cardFocused = true
                }
            }
        }
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 2) {
            Text("Flash Cards")
                .font(.system(size: 16, weight: .semibold, design: .rounded))
                .foregroundStyle(AppTheme.gold)
            Text("Reveal, then rate your recall")
                .font(.system(size: 26, weight: .bold, design: .rounded))
                .foregroundStyle(.white)
        }
    }

    private var statBar: some View {
        HStack(spacing: 18) {
            ScoreChip(value: "\(viewModel.knownCount)", label: "Known", tint: AppTheme.success, compact: true)
            ScoreChip(value: "\(viewModel.reviewCount)", label: "Review", tint: AppTheme.failure, compact: true)
            ScoreChip(value: viewModel.progressText, label: "Progress", compact: true)
        }
        .fixedSize()
        .padding(.horizontal, 18)
        .padding(.vertical, 10)
        .background(Capsule().fill(Color.white.opacity(0.08)))
        .overlay(Capsule().stroke(AppTheme.cardBorder, lineWidth: 1))
    }

    private var startPrompt: some View {
        VStack(spacing: 24) {
            Image(systemName: "rectangle.stack.fill")
                .font(.system(size: 56))
                .foregroundStyle(.white.opacity(0.85))
            Text("Ready to review some words?")
                .font(.system(size: 30, weight: .semibold, design: .rounded))
                .foregroundStyle(.white)
            Text("A session of \(min(FlashCardViewModel.sessionSize, store.words.count)) random cards")
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

    @ViewBuilder
    private var sessionView: some View {
        if let word = viewModel.currentCard {
            VStack(spacing: 26) {
                FlashCardTile(word: word, isFlipped: viewModel.isFlipped) {
                    viewModel.flip()
                }
                .frame(maxWidth: 1200)
                .focused($cardFocused)
                .prefersDefaultFocus(true, in: namespace)

                if viewModel.isFlipped {
                    HStack(spacing: 24) {
                        Button {
                            viewModel.markNeedsReview()
                        } label: {
                            Label("Still Learning", systemImage: "arrow.counterclockwise")
                                .font(.system(size: 24, weight: .bold, design: .rounded))
                                .padding(.horizontal, 36)
                                .padding(.vertical, 16)
                        }
                        .buttonStyle(.card)
                        .tint(AppTheme.failure)
                        .focused($reviewButtonFocused)

                        Button {
                            viewModel.markKnown()
                        } label: {
                            Label("Got It", systemImage: "checkmark")
                                .font(.system(size: 24, weight: .bold, design: .rounded))
                                .padding(.horizontal, 36)
                                .padding(.vertical, 16)
                        }
                        .buttonStyle(.card)
                        .tint(AppTheme.success)
                    }
                }
            }
        }
    }

    private var summaryView: some View {
        VStack(spacing: 22) {
            Image(systemName: "star.fill")
                .font(.system(size: 56))
                .foregroundStyle(AppTheme.gold)
            Text("Session Complete!")
                .font(.system(size: 34, weight: .bold, design: .rounded))
                .foregroundStyle(.white)

            HStack(spacing: 40) {
                summaryStat(value: "\(viewModel.knownCount)", label: "Known", tint: AppTheme.success)
                summaryStat(value: "\(viewModel.reviewCount)", label: "Still Learning", tint: AppTheme.failure)
                summaryStat(value: "\(viewModel.deck.count)", label: "Total", tint: .white)
            }
            .padding(.vertical, 10)

            Button {
                viewModel.start()
            } label: {
                Text("New Session")
                    .font(.system(size: 26, weight: .bold, design: .rounded))
                    .padding(.horizontal, 52)
                    .padding(.vertical, 16)
            }
            .buttonStyle(.card)
            .tint(AppTheme.periwinkle)
            .prefersDefaultFocus(true, in: namespace)
        }
    }

    private func summaryStat(value: String, label: String, tint: Color) -> some View {
        VStack(spacing: 6) {
            Text(value)
                .font(.system(size: 40, weight: .bold, design: .rounded))
                .foregroundStyle(tint)
            Text(label.uppercased())
                .font(.system(size: 15, weight: .semibold))
                .tracking(1.1)
                .foregroundStyle(.white.opacity(0.6))
        }
    }
}
