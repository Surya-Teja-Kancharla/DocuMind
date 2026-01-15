import { useRef } from "react";

const ChatInput = ({
  value,
  onChange,
  onSend,
  disabled,
  attachments,
  onUpload,
  onRemove,
}) => {
  const fileRef = useRef(null);

  return (
    <div className="w-full max-w-3xl mx-auto">
      <div className="bg-[#2f2f2f] rounded-2xl px-4 py-3 flex flex-col gap-2 shadow-xl">

        {/* Attachment chips */}
        {attachments.length > 0 && (
          <div className="flex gap-2 flex-wrap">
            {attachments.map((file, idx) => (
              <div
                key={idx}
                className="flex items-center gap-2 bg-[#3a3a3a] px-3 py-1.5 rounded-lg"
              >
                <span className="text-xs text-white truncate max-w-[160px]">
                  {file.name}
                </span>
                <button
                  onClick={() => onRemove(idx)}
                  className="text-red-400 hover:text-red-300"
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
        )}

        <div className="flex items-center gap-3">
          <button
            onClick={() => fileRef.current.click()}
            className="text-xl text-gray-400 hover:text-white"
            title="Upload document"
          >
            +
          </button>

          <input
            ref={fileRef}
            type="file"
            accept=".pdf,.docx,.txt"
            multiple
            hidden
            onChange={onUpload}
          />

          <input
            value={value}
            onChange={onChange}
            onKeyDown={(e) => e.key === "Enter" && onSend()}
            disabled={disabled}
            placeholder="Ask anything"
            className="flex-1 bg-transparent outline-none text-white placeholder-gray-400"
          />

          <button
            onClick={onSend}
            disabled={disabled}
            className="bg-blue-600 hover:bg-blue-500 text-white rounded-full w-9 h-9 flex items-center justify-center transition"
          >
            ↑
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInput;
