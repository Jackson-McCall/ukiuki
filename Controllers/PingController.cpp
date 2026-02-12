#include "PingController.h"

void PingController::healthCheck(const drogon::HttpRequestPtr& req,
	std::function<void(const drogon::HttpResponsePtr&)>&& callback) {

	// Log to the console so we know the application is healthy
	LOG_INFO << "UkiUki API connection is healthy.";

	// HttpResponse::newHttpResponse() allocates a response object on the heap
	// and returns a shared_ptr to it
	auto resp = drogon::HttpResponse::newHttpResponse();

	// Set the HTTP Status code to 200
	resp->setStatusCode(drogon::k200OK);

	// Set the body content
	resp->setBody("UkiUkiAPI health status = UP");

	// CORS (Cross-Origin Resource Sharing) blocks requests from different origins than the API
	// Add CORS headers, since this is health, anyone can check
	resp->addHeader("Access-Control-Allow-Origin", "*");

	// Invoke the callback. This sends the response through the socket 
	callback(resp);
}