import SwiftUI

struct SpellItView: View {
    let store: WordStore
    @StateObject private var viewModel: SpellItViewModel
    @Namespace private var namespace
    @FocusState private var focusedLetter: Character?

    private static let alphabet: [Character] = Array("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    init(store: WordStore) {
        self.store = store
        _viewModel = StateObject(wrappedValue: SpellItViewModel(store: store))
    }

    var body: some View {
        ZStack {
            AppBackground()

            VStack(spacing: 14) {
                HStack(alignment: .center) {
                    header
                    Spacer()
                    if viewModel.hasStarted {
                        scoreBar
                    }
                }

                Spacer(minLength: 0)

                if viewModel.hasStarted, let word = viewModel.currentWord {
                    content(for: word)
                } else {
                    startPrompt
                }

                Spacer(minLength: 0)
            }
            .padding(.top, 30)
            .padding(.horizontal, 90)
            .padding(.bottom, 30)
            .disabled(viewModel.showExplanation)

            if viewModel.showExplanation, let word = viewModel.currentWord {
                WordExplanationModal(
                    word: word,
                    isCorrect: viewModel.isCorrectSelection,
                    onNext: { viewModel.advanceToNext() }
                )
                .padding(60)
            }
        }
        .animation(.easeInOut(duration: 0.25), value: viewModel.showExplanation)
        .onChange(of: viewModel.currentWord?.word) { _, _ in
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.05) {
                focusedLetter = "A"
            }
        }
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 2) {
            Text("Spell It")
                .font(.system(size: 16, weight: .semibold, design: .rounded))
                .foregroundStyle(AppTheme.gold)
            Text("Guess the word from its meaning")
                .font(.system(size: 26, weight: .bold, design: .rounded))
                .foregroundStyle(.white)
        }
    }

    private var scoreBar: some View {
        HStack(spacing: 18) {
            ScoreChip(value: "\(viewModel.solvedCount)", label: "Solved", tint: AppTheme.success, compact: true)
            ScoreChip(value: "\(viewModel.attemptedCount)", label: "Attempts", compact: true)
            ScoreChip(value: "\(viewModel.livesRemaining)", label: "Lives", tint: AppTheme.gold, compact: true)
        }
        .fixedSize()
        .padding(.horizontal, 18)
        .padding(.vertical, 10)
        .background(Capsule().fill(Color.white.opacity(0.08)))
        .overlay(Capsule().stroke(AppTheme.cardBorder, lineWidth: 1))
    }

    private var startPrompt: some View {
        VStack(spacing: 24) {
            Image(systemName: "textformat.abc")
                .font(.system(size: 56))
                .foregroundStyle(.white.opacity(0.85))
            Text("See the meaning, guess the word")
                .font(.system(size: 30, weight: .semibold, design: .rounded))
                .foregroundStyle(.white)
            Text("\(SpellItViewModel.maxLives) wrong guesses allowed per word")
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
    private func content(for word: Word) -> some View {
        VStack(spacing: 24) {
            GlassCard {
                Text(word.meaning)
                    .font(.system(size: 26, weight: .medium))
                    .foregroundStyle(.white)
                    .multilineTextAlignment(.center)
                    .lineLimit(3)
                    .minimumScaleFactor(0.8)
                    .padding(.vertical, 24)
                    .padding(.horizontal, 34)
                    .frame(maxWidth: .infinity)
            }
            .frame(maxWidth: 1100)

            maskedWordView

            letterGrid
        }
    }

    private var maskedWordView: some View {
        HStack(spacing: 10) {
            ForEach(Array(viewModel.maskedLetters.enumerated()), id: \.offset) { _, letter in
                Text(String(letter))
                    .font(.system(size: 34, weight: .heavy, design: .rounded))
                    .foregroundStyle(letter == "_" ? .white.opacity(0.35) : (viewModel.isFailed ? AppTheme.failure : .white))
                    .frame(width: 34)
                    .overlay(alignment: .bottom) {
                        Rectangle()
                            .fill(.white.opacity(0.4))
                            .frame(height: 3)
                            .offset(y: 6)
                    }
            }
        }
    }

    private var letterGrid: some View {
        LazyVGrid(columns: Array(repeating: GridItem(.fixed(64), spacing: 10), count: 13), spacing: 10) {
            ForEach(Self.alphabet, id: \.self) { letter in
                Button {
                    viewModel.guess(letter)
                } label: {
                    Text(String(letter))
                }
                .buttonStyle(LetterButtonStyle(state: letterState(letter)))
                .disabled(viewModel.guessedLetters.contains(letter) || viewModel.isRoundOver)
                .focused($focusedLetter, equals: letter)
            }
        }
    }

    private func letterState(_ letter: Character) -> LetterState {
        guard viewModel.guessedLetters.contains(letter) else { return .neutral }
        guard let word = viewModel.currentWord else { return .neutral }
        return word.word.uppercased().contains(letter) ? .correct : .wrong
    }
}
