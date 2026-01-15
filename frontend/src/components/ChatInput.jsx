import { useRef } from "react";

const ChatInput = ({
  value,
  onChange,
  onSend,
  disabled,
  attachment,
  onUpload,
  onRemoveAttachment
}) => {
  const fileRef = useRef(null);

  return (
    <div className="w-full max-w-3xl mx-auto">
      <div className="bg-[#2f2f2f] rounded-2xl px-4 py-3 flex flex-col gap-2 shadow-lg">

        {/* Attachment chip */}
        {attachment && (
          <div className="flex items-center gap-3 bg-[#3a3a3a] px-3 py-2 rounded-lg w-fit">
            <div className="w-8 h-8 rounded bg-red-500 flex items-center justify-center text-white text-sm">
              PDF
            </div>

            <div className="text-sm text-white max-w-[180px] truncate">
              {attachment.name}
            </div>

            <button
              onClick={onRemoveAttachment}
              className="text-white hover:text-red-400"
            >
              ✕
            </button>
          </div>
        )}

        {/* Input row */}
        <div className="flex items-center gap-3">
          {/* Plus button */}
          <button
            onClick={() => fileRef.current.click()}
            className="text-gray-400 hover:text-white text-xl"
            title="Upload document"
          >
            +
          </button>

          <input
            ref={fileRef}
            type="file"
            accept=".pdf,.txt,.docx"
            hidden
            onChange={onUpload}
          />

          <input
            value={value}
            onChange={onChange}
            onKeyDown={e => e.key === "Enter" && onSend()}
            placeholder="Ask anything"
            disabled={disabled}
            className="flex-1 bg-transparent outline-none text-white placeholder-gray-400"
          />

          <button
            onClick={onSend}
            disabled={disabled}
            className="bg-blue-600 hover:bg-blue-700 text-white rounded-full w-9 h-9 flex items-center justify-center"
          >
            ↑
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInput;
