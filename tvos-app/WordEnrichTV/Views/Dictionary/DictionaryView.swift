import SwiftUI

struct DictionaryView: View {
    @StateObject private var viewModel: DictionaryViewModel
    @FocusState private var focusedWordID: String?
    @FocusState private var searchFieldFocused: Bool
    @Namespace private var namespace

    init(store: WordStore) {
        _viewModel = StateObject(wrappedValue: DictionaryViewModel(store: store))
    }

    var body: some View {
        ZStack {
            AppBackground()

            VStack(alignment: .leading, spacing: 20) {
                header

                HStack(alignment: .top, spacing: 28) {
                    wordListPane
                        .frame(width: 600)

                    Group {
                        if let word = viewModel.selectedWord, !viewModel.filteredWords.isEmpty {
                            WordDetailPane(word: word)
                        } else {
                            DictionaryEmptyState()
                        }
                    }
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
                }
            }
            .padding(.top, 40)
            .padding(.horizontal, 90)
            .padding(.bottom, 40)
        }
        .onChange(of: focusedWordID) { _, newValue in
            guard let id = newValue,
                  let word = viewModel.filteredWords.first(where: { $0.id == id }) else { return }
            viewModel.select(word)
        }
    }

    private var header: some View {
        HStack(alignment: .firstTextBaseline) {
            VStack(alignment: .leading, spacing: 4) {
                Text("Dictionary")
                    .font(.system(size: 36, weight: .bold, design: .rounded))
                    .foregroundStyle(.white)
                Text("\(viewModel.filteredWords.count.formatted()) of \(viewModel.sortedWords.count.formatted()) words")
                    .font(.system(size: 17))
                    .foregroundStyle(.white.opacity(0.55))
            }
            Spacer()
        }
    }

    private var wordListPane: some View {
        VStack(spacing: 14) {
            searchField

            ScrollViewReader { proxy in
                HStack(alignment: .top, spacing: 6) {
                    ScrollView(showsIndicators: false) {
                        LazyVStack(alignment: .leading, spacing: 10, pinnedViews: [.sectionHeaders]) {
                            ForEach(viewModel.sections) { section in
                                Section {
                                    ForEach(section.words) { word in
                                        Button {
                                            viewModel.select(word)
                                        } label: {
                                            Text(word.word.capitalized)
                                        }
                                        .buttonStyle(DictionaryRowButtonStyle(isSelected: viewModel.selectedWord == word))
                                        .focused($focusedWordID, equals: word.id)
                                    }
                                } header: {
                                    LetterSectionHeader(letter: section.letter)
                                        .id("section-\(section.letter)")
                                }
                            }
                        }
                        .padding(.bottom, 20)
                    }
                    .frame(maxWidth: .infinity)
                    .focusSection()

                    Group {
                        if viewModel.searchText.isEmpty && viewModel.availableLetters.count > 3 {
                            AlphabetRail(letters: viewModel.availableLetters) { letter in
                                withAnimation {
                                    proxy.scrollTo("section-\(letter)", anchor: .top)
                                }
                            }
                        } else {
                            Color.clear
                        }
                    }
                    .frame(width: 34)
                    .focusSection()
                }
            }
        }
    }

    private var searchField: some View {
        HStack(spacing: 12) {
            Image(systemName: "magnifyingglass")
                .foregroundStyle(.white.opacity(0.55))
            TextField("Search words", text: $viewModel.searchText)
                .textFieldStyle(.plain)
                .foregroundStyle(.white)
                .focused($searchFieldFocused)
                .prefersDefaultFocus(true, in: namespace)

            if !viewModel.searchText.isEmpty {
                Button {
                    viewModel.searchText = ""
                } label: {
                    Image(systemName: "xmark.circle.fill")
                        .foregroundStyle(.white.opacity(0.55))
                }
                .buttonStyle(.plain)
            }
        }
        .padding(.horizontal, 20)
        .padding(.vertical, 14)
        .background(
            RoundedRectangle(cornerRadius: 18, style: .continuous)
                .fill(Color.white.opacity(0.08))
        )
        .overlay(
            RoundedRectangle(cornerRadius: 18, style: .continuous)
                .stroke(searchFieldFocused ? Color.white : AppTheme.cardBorder, lineWidth: searchFieldFocused ? 3 : 1)
        )
    }
}

struct LetterSectionHeader: View {
    let letter: String

    var body: some View {
        Text(letter)
            .font(.system(size: 17, weight: .bold, design: .rounded))
            .foregroundStyle(AppTheme.gold)
            .padding(.horizontal, 20)
            .padding(.vertical, 6)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(
                Rectangle()
                    .fill(.ultraThinMaterial)
                    .background(AppTheme.ink.opacity(0.75))
            )
    }
}

struct AlphabetRail: View {
    let letters: [String]
    let onSelect: (String) -> Void

    var body: some View {
        VStack(spacing: 2) {
            ForEach(letters, id: \.self) { letter in
                Button {
                    onSelect(letter)
                } label: {
                    Text(letter)
                }
                .buttonStyle(RailButtonStyle())
            }
        }
    }
}
