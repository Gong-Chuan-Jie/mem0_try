from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from mem0 import Memory

openai_client = OpenAI()
memory = Memory()

def chat_with_memories(message: str, user_id: str = "default_user") -> str:
    # Retrieve relevant memories
    relevant_memories = memory.search(query=message, user_id=user_id, limit=3)
    if relevant_memories["results"]:
        print("✅ 命中相关记忆:")
        for i, entry in enumerate(relevant_memories["results"], 1):
            print(f"{i}. {entry['memory']}")
    else:
        print("⚠️ 没有命中相关记忆")  # 👈 打印相关记忆结构

    memories_str = "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])

    # Generate Assistant response
    system_prompt = f"You are a helpful AI. Answer the question based on query and memories.\nUser Memories:\n{memories_str}"
    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": system_prompt}, 
        {"role": "user", "content": message}
    ]
    response = openai_client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    assistant_response = response.choices[0].message.content

    # Create new memories from the conversation (only user + assistant, no system)
    if assistant_response:
        memory.add([
            {"role": "user", "content": message},
            {"role": "assistant", "content": assistant_response}
        ], user_id=user_id)

    # Print all memories for debugging
    all_memories = memory.get_all(user_id=user_id)
    print(f"\n🔍 当前存储的记忆数量: {len(all_memories['results'])}")
    for i, entry in enumerate(all_memories["results"], 1):
        print(f"{i}. {entry['memory']}")

    return assistant_response or ""

def main():
    print("Chat with AI (type 'exit' to quit)")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        print(f"AI: {chat_with_memories(user_input)}")

if __name__ == "__main__":
    main()
