import chromadb

from sentence_transformers import SentenceTransformer, CrossEncoder

# Connect to the existing ChromaDB database
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Load the stored club collection
collection = chroma_client.get_collection(name="clubs")

# Load the same Sentence-BERT model used for embeddings
# model = SentenceTransformer("all-MiniLM-L6-v2")
# model = SentenceTransformer("all-mpnet-base-v2")
bi_encoder = SentenceTransformer("paraphrase-MiniLM-L6-v2")

cross_encoder = CrossEncoder("cross-encoder/ms-marco-TinyBERT-L-6")

query_text = "singing club"
query_embedding = bi_encoder.encode([query_text]).tolist()

threshold = 0.5

# Search for the most similar clubs
results = collection.query(
    query_embeddings=query_embedding,
    n_results=50  # Get top 5 similar clubs
)

filtered_results = [
    (club, distance) for club, distance in zip(results["metadatas"][0], results["distances"][0])
    if 1-distance > threshold  # Only keep relevant results
]

# Use cross-encoder to re-rank the filtered results
reranked_results = []
for club, distance in filtered_results:
    # Create pair (query, club description)
    pair = [query_text, club['Description']]
    # Get cross-encoder score (relevance score)
    score_tensor = cross_encoder.predict(pair)  # Encoding the pair using cross-encoder
    
    # Access the scalar value from the tensor
    score = score_tensor.item()
    
    reranked_results.append((club, score))

# Sort results by the cross-encoder score (higher is better)
reranked_results = sorted(reranked_results, key=lambda x: x[1], reverse=True)

# print(results)
print(f"\n🔍 Query: {query_text} - Found {len(reranked_results)} relevant clubs:\n")

# Print the results
for i, (club, score) in enumerate(reranked_results):
    print(f"Result {i+1}:")
    print(f"Name: {club['Name']}")
    print(f"Categories: {club['CategoryNames']}")
    print(f"Description: {club['Description']}")
    print(f"Similarity Score: {score:.4f}")
    print("-" * 50)

