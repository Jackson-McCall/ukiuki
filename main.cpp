#include <drogon/drogon.h>

using namespace drogon;

int main() {
	// Set logging level to see exactly what Drogon is doing
	trantor::Logger::setLogLevel(trantor::Logger::kInfo);

	// LOG_INFO is Drogon's internal logging macro, it's thread-safe
	// In a professional C++ backend, we never use std::cout because if two threads try to print at the
	// same time, the text gets jumbled. LOG_INFO handles the queueing for us.
	LOG_INFO << "UkiUki API is starting...";

	// app().addListener - opens a socket on our network card
	// 127.0.0.1 means only my computer can talk to it, 0.0.0.0 means the whole internet can
	drogon::app()
		.addListener("127.0.0.1", 8080)
		// I can add global configs here, like thread count
		//.setThreadNum(0) // 0 means drogon picks based on my CPU cores
		// This is a blocking call. The program stays here until I kill it.
		// Drogon uses this to automatically search the entire compiled binary for any
		// class that inherits from HttpController, then it auto-connects them
		.run();

	return 0;
}