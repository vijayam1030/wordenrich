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

            VStack(spacing: 0) {
                header
                    .padding(.top, 36)
                    .padding(.bottom, 18)

                GlassCard {
                    HStack(spacing: 0) {
                        ScoreChip(value: "\(viewModel.correctCount)", label: "Correct", tint: AppTheme.success)
                        Divider().overlay(Color.white.opacity(0.15))
                        ScoreChip(value: "\(viewModel.totalCount)", label: "Total")
                        Divider().overlay(Color.white.opacity(0.15))
                        ScoreChip(value: "\(viewModel.streak)", label: "Streak", tint: AppTheme.gold)
                        Divider().overlay(Color.white.opacity(0.15))
                        ScoreChip(value: "\(viewModel.accuracy)%", label: "Accuracy")
                    }
                    .padding(.vertical, 18)
                    .padding(.horizontal, 20)
                }
                .frame(maxWidth: 1100)
                .padding(.bottom, 22)

                if viewModel.hasStarted, let word = viewModel.currentWord {
                    ScrollView(showsIndicators: false) {
                        content(for: word)
                            .padding(.bottom, 10)
                    }
                    .frame(maxWidth: .infinity, maxHeight: .infinity)

                    if viewModel.isAnswered {
                        Button {
                            viewModel.nextQuestion()
                        } label: {
                            Text("Next Word")
                                .font(.system(size: 24, weight: .bold, design: .rounded))
                                .padding(.horizontal, 44)
                                .padding(.vertical, 14)
                        }
                        .buttonStyle(.card)
                        .tint(AppTheme.periwinkle)
                        .prefersDefaultFocus(true, in: namespace)
                        .padding(.top, 14)
                        .padding(.bottom, 30)
                    }
                } else {
                    startPrompt
                    Spacer(minLength: 0)
                }
            }
            .padding(.horizontal, 90)
        }
    }

    private var header: some View {
        VStack(spacing: 4) {
            Text("Learn Mode")
                .font(.system(size: 22, weight: .semibold, design: .rounded))
                .foregroundStyle(AppTheme.gold)
            Text("What does the word mean?")
                .font(.system(size: 36, weight: .bold, design: .rounded))
                .foregroundStyle(.white)
        }
    }

    private var startPrompt: some View {
        VStack(spacing: 28) {
            Image(systemName: "brain.head.profile")
                .font(.system(size: 64))
                .foregroundStyle(.white.opacity(0.85))
            Text("Ready to build your vocabulary?")
                .font(.system(size: 32, weight: .semibold, design: .rounded))
                .foregroundStyle(.white)
            Text("\(store.words.count) words loaded")
                .font(.system(size: 20))
                .foregroundStyle(.white.opacity(0.6))

            Button {
                viewModel.start()
            } label: {
                Text("Start")
                    .font(.system(size: 28, weight: .bold, design: .rounded))
                    .padding(.horizontal, 56)
                    .padding(.vertical, 18)
            }
            .buttonStyle(.card)
            .tint(AppTheme.periwinkle)
            .prefersDefaultFocus(true, in: namespace)
        }
        .padding(60)
    }

    @ViewBuilder
    private func content(for word: Word) -> some View {
        VStack(spacing: 24) {
            GlassCard {
                Text(word.word.capitalized)
                    .font(.system(size: 50, weight: .heavy, design: .rounded))
                    .foregroundStyle(.white)
                    .padding(.vertical, 28)
                    .frame(maxWidth: .infinity)
            }
            .frame(maxWidth: 1000)

            if viewModel.isAnswered {
                resultDetail(for: word)
            } else {
                optionsGrid
            }
        }
        .id(word.word)
        .transition(.asymmetric(
            insertion: .opacity.combined(with: .scale(scale: 0.97)),
            removal: .opacity
        ))
        .animation(.easeInOut(duration: 0.25), value: word.word)
    }

    private var optionsGrid: some View {
        LazyVGrid(columns: [GridItem(.flexible(), spacing: 24), GridItem(.flexible(), spacing: 24)], spacing: 24) {
            ForEach(Array(viewModel.options.enumerated()), id: \.element) { index, option in
                Button {
                    viewModel.select(option)
                } label: {
                    Text(option)
                }
                .buttonStyle(OptionButtonStyle(state: viewModel.state(for: option)))
                .focused($focusedField, equals: option)
                .prefersDefaultFocus(index == 0, in: namespace)
            }
        }
        .frame(maxWidth: 1200)
    }

    private func resultDetail(for word: Word) -> some View {
        VStack(spacing: 18) {
            HStack(spacing: 16) {
                Image(systemName: viewModel.isCorrectSelection ? "checkmark.circle.fill" : "xmark.circle.fill")
                    .font(.system(size: 30))
                    .foregroundStyle(viewModel.isCorrectSelection ? AppTheme.success : AppTheme.failure)
                Text(viewModel.isCorrectSelection ? "Correct!" : "Not quite")
                    .font(.system(size: 28, weight: .bold, design: .rounded))
                    .foregroundStyle(.white)
                Spacer()
            }

            GlassCard {
                VStack(alignment: .leading, spacing: 18) {
                    Text(word.meaning)
                        .font(.system(size: 24, weight: .medium))
                        .foregroundStyle(.white.opacity(0.95))

                    if !word.synonyms.isEmpty {
                        labeledChips(title: "Synonyms", items: word.synonyms, tint: AppTheme.success)
                    }
                    if !word.antonyms.isEmpty {
                        labeledChips(title: "Antonyms", items: word.antonyms, tint: AppTheme.failure)
                    }
                    if let sentence = word.sentences.first {
                        VStack(alignment: .leading, spacing: 6) {
                            Text("Example".uppercased())
                                .font(.system(size: 14, weight: .semibold))
                                .tracking(1.1)
                                .foregroundStyle(.white.opacity(0.5))
                            Text("\u{201C}\(sentence)\u{201D}")
                                .font(.system(size: 20, weight: .regular))
                                .italic()
                                .foregroundStyle(.white.opacity(0.85))
                        }
                    }
                    if !word.origin.isEmpty {
                        VStack(alignment: .leading, spacing: 6) {
                            Text("Origin".uppercased())
                                .font(.system(size: 14, weight: .semibold))
                                .tracking(1.1)
                                .foregroundStyle(.white.opacity(0.5))
                            Text(word.origin)
                                .font(.system(size: 18))
                                .foregroundStyle(.white.opacity(0.7))
                        }
                    }
                }
                .padding(26)
            }
            .frame(maxWidth: 1100)
        }
        .frame(maxWidth: 1100)
    }

    private func labeledChips(title: String, items: [String], tint: Color) -> some View {
        VStack(alignment: .leading, spacing: 10) {
            Text(title.uppercased())
                .font(.system(size: 14, weight: .semibold))
                .tracking(1.1)
                .foregroundStyle(.white.opacity(0.5))
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 10) {
                    ForEach(items, id: \.self) { item in
                        WordChip(text: item, tint: tint)
                    }
                }
            }
        }
    }
}
