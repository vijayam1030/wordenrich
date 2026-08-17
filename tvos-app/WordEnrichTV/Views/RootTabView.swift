import SwiftUI

struct RootTabView: View {
    @StateObject private var store = WordStore()

    var body: some View {
        TabView {
            LearnView(store: store)
                .tabItem { Label("Learn", systemImage: "brain.head.profile") }

            FlashCardView(store: store)
                .tabItem { Label("Flash Cards", systemImage: "rectangle.stack.fill") }

            MemoryMatchView(store: store)
                .tabItem { Label("Memory Match", systemImage: "square.grid.3x3.fill") }

            DictionaryView(store: store)
                .tabItem { Label("Dictionary", systemImage: "text.book.closed.fill") }
        }
    }
}
