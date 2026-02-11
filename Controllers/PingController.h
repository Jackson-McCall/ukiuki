#pragma once

#include <drogon/HttpController.h>

/**
 * We inherit from HttpController using CRTP (Curiously Recurring Template
 * Pattern). This allows Drogon to perform static polymorphism for better
 * performance.
 */
class PingController : public drogon::HttpController<PingController> {
public:
	/**
	 * The METHOD_LIST macros define the routing table for this specific class.
	 */
	METHOD_LIST_BEGIN
		// Use the ADD_METHOD_TO macro:
		// 1. The function name
		// 2. The URI path (this will be http://localhost:8080/health)
		// 3. Constraints (HTTP Get only)
		ADD_METHOD_TO(PingController::healthCheck, "/health", drogon::Get);
	METHOD_LIST_END

		/**
		* Signature Breakdown:
		* 1. const HttpRequestPtr &req: A shared pointer to the incoming data.
		* Shared pointers prevent memory leaks by counting references
		* 2. std::function<void(const HttpResponsePtr &)> &&callback:
		* an r-value reference to a function. We use '&&' to move the callback
		* instead of copying it, which is faster.
		*
		*/
		void healthCheck(const drogon::HttpRequestPtr& req,
			std::function<void(const drogon::HttpResponsePtr&)>&& callback);
};