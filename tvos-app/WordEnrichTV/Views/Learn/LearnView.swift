import SwiftUI

struct LearnView: View {
    let store: WordStore
    @StateObject private var viewModel: LearnGameViewModel
    @FocusState private var focusedField: String?
    @Namespace private var namespace

    init(store: WordStore) {
        self.store = store
        _viewModel = StateObject(wrappedValue: LearnGameViewModel(store: store))
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
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 2) {
            Text("Learn Mode")
                .font(.system(size: 16, weight: .semibold, design: .rounded))
                .foregroundStyle(AppTheme.gold)
            Text("What does the word mean?")
                .font(.system(size: 26, weight: .bold, design: .rounded))
                .foregroundStyle(.white)
        }
    }

    private var scoreBar: some View {
        HStack(spacing: 18) {
            ScoreChip(value: "\(viewModel.correctCount)", label: "Correct", tint: AppTheme.success, compact: true)
            ScoreChip(value: "\(viewModel.totalCount)", label: "Total", compact: true)
            ScoreChip(value: "\(viewModel.streak)", label: "Streak", tint: AppTheme.gold, compact: true)
            ScoreChip(value: "\(viewModel.accuracy)%", label: "Accuracy", compact: true)
        }
        .fixedSize()
        .padding(.horizontal, 18)
        .padding(.vertical, 10)
        .background(
            Capsule().fill(Color.white.opacity(0.08))
        )
        .overlay(
            Capsule().stroke(AppTheme.cardBorder, lineWidth: 1)
        )
    }

    private var startPrompt: some View {
        VStack(spacing: 24) {
            Image(systemName: "brain.head.profile")
                .font(.system(size: 56))
                .foregroundStyle(.white.opacity(0.85))
            Text("Ready to build your vocabulary?")
                .font(.system(size: 30, weight: .semibold, design: .rounded))
                .foregroundStyle(.white)
            Text("\(store.words.count) words loaded")
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
        VStack(spacing: 32) {
            GlassCard {
                Text(word.word.capitalized)
                    .font(.system(size: 54, weight: .heavy, design: .rounded))
                    .foregroundStyle(.white)
                    .padding(.vertical, 30)
                    .frame(maxWidth: .infinity)
            }
            .frame(maxWidth: 1000)

            optionsGrid

            nextWordButton
        }
        .id(word.word)
    }

    private var optionsGrid: some View {
        LazyVGrid(columns: [GridItem(.flexible(), spacing: 22), GridItem(.flexible(), spacing: 22)], spacing: 22) {
            ForEach(Array(viewModel.options.enumerated()), id: \.element) { index, option in
                Button {
                    viewModel.select(option)
                } label: {
                    Text(option)
                }
                .buttonStyle(OptionButtonStyle(state: viewModel.state(for: option)))
                .focused($focusedField, equals: option)
                .disabled(viewModel.isAnswered)
                .prefersDefaultFocus(index == 0, in: namespace)
            }
        }
        .frame(maxWidth: 1200)
    }

    private var nextWordButton: some View {
        Button {
            viewModel.advanceToNext()
        } label: {
            Text("Next Word")
                .font(.system(size: 24, weight: .bold, design: .rounded))
                .padding(.horizontal, 44)
                .padding(.vertical, 14)
        }
        .buttonStyle(.card)
        .tint(AppTheme.periwinkle)
        .disabled(!viewModel.isAnswered)
        .opacity(viewModel.isAnswered ? 1.0 : 0.4)
    }
}
