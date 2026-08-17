import SwiftUI

struct RootTabView: View {
    @StateObject private var store = WordStore()

    var body: some View {
        TabView {
            LearnView(store: store)
                .tabItem { Label("Learn", systemImage: "brain.head.profile") }

            ComingSoonView(
                title: "Speed Challenge",
                subtitle: "Race the clock and match as many words as you can before time runs out.",
                systemImage: "bolt.fill"
            )
            .tabItem { Label("Speed", systemImage: "bolt.fill") }

            ComingSoonView(
                title: "Quiz Mode",
                subtitle: "A graded ten-question run that ends with a final score and letter grade.",
                systemImage: "checkmark.seal.fill"
            )
            .tabItem { Label("Quiz", systemImage: "checkmark.seal.fill") }

            ComingSoonView(
                title: "Word Battle",
                subtitle: "Two players, one remote, one couch. First to five correct answers wins.",
                systemImage: "person.2.fill"
            )
            .tabItem { Label("Battle", systemImage: "person.2.fill") }

            ComingSoonView(
                title: "Endurance",
                subtitle: "Three lives and rising difficulty. See how far your vocabulary can take you.",
                systemImage: "flame.fill"
            )
            .tabItem { Label("Endure", systemImage: "flame.fill") }

            ComingSoonView(
                title: "Dictionary",
                subtitle: "Browse and search the full word list with meanings, synonyms, and origins.",
                systemImage: "text.book.closed.fill"
            )
            .tabItem { Label("Dictionary", systemImage: "text.book.closed.fill") }
        }
    }
}
