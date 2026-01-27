def assemble_context(chunks: list) -> str:
    if not chunks:
        return ""

    blocks = []
    for i, c in enumerate(chunks, start=1):
        blocks.append(f"Source {i}:\n{c['text']}")

    return "\n\n---\n\n".join(blocks)
