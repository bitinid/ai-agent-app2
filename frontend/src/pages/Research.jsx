import Chat from "../components/Chat";

function Research() {
  const initialMessage =
    "Hello! How can I help you today?";

  return (
    <div>
      <div className="flex flex-col md:flex-row gap-8 mb-12">
        
        <div className="md:w-2/3">
          <div className="bg-white rounded-lg shadow-md overflow-hidden">
            <div className="p-6">
              <h5 className="text-xl font-semibold mb-2">
                Chat with Didi, Demo Agent.
              </h5>
              <p className="text-blue-600 mb-4">
              Ask Didi anything about technology, and He'll do his best to assist you!
              </p>
              <Chat
                agentType="research"
                initialMessage={initialMessage}
                agentInitials="DIDI"
              />
            </div>
          </div>
        </div>
      </div>


    </div>
  );
}

export default Research;