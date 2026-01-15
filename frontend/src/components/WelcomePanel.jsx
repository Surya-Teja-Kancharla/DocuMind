const WelcomePanel = () => {
  return (
    <div className="flex flex-col items-center justify-center h-full text-white">
      <h1 className="text-3xl font-semibold mb-6">
        Welcome to DocuMind
      </h1>

      <p className="mt-4 text-sm text-slate-400">
        AI can make mistakes. Verify important information.
      </p>
    </div>
  );
};

export default WelcomePanel;
