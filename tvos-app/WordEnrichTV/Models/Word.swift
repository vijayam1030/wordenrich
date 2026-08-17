import Foundation

struct Word: Codable, Identifiable, Hashable {
    var id: String { word }
    let word: String
    let meaning: String
    let synonyms: [String]
    let antonyms: [String]
    let sentences: [String]
    let origin: String
}
