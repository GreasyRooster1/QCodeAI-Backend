#[macro_use] extern crate rocket;

use std::env;
use std::sync::Arc;
use openrouter_rust::{ChatCompletionBuilder, OpenRouterClient};
use rocket::fairing::{Fairing, Info, Kind};
use rocket::{Request, Response};
use rocket::http::Header;
use rocket::serde::json::Json;
use rocket::serde::{Deserialize, Serialize};
use rocket_firebase_auth::{FirebaseAuth, FirebaseToken};
use async_openai::{
    types::{CreateChatCompletionRequestArgs, ChatCompletionRequestUserMessageArgs},
    Client,
};
use dotenvy::dotenv;
use serde_json::json;

struct ServerState {
    auth: FirebaseAuth,
}

#[derive(Serialize,Deserialize)]
struct AIResponse{
    output:String,
}
#[derive(Serialize,Deserialize)]
struct AIRequest {
    provider: Option<String>,
    system_prompt: Option<String>,
    user_prompt: Option<String>,
    temperature: Option<f32>,
    top_p: Option<f32>,
    frequency_penalty: Option<f32>,
    max_tokens: Option<f32>,
}

#[launch]
async fn rocket() -> _ {
    dotenv().unwrap();
    let firebase_auth = FirebaseAuth::builder()
        .json_file("service-account.json")
        .build()
        .unwrap();

    rocket::build()
    .mount("/",routes![status,all_options])
    .mount("/api", routes![
        generate
    ])
    .manage(firebase_auth)
    .attach(CORS)
}

#[get("/")]
fn status() -> &'static str {
    "running"
}

#[post("/ai/generate",format = "json", data = "<req>")]
async fn generate(token: FirebaseToken,req: Json<AIRequest>) -> Result<Json<AIResponse>, String> {
    let client = OpenRouterClient::builder()
        .api_key(env::var("OPENROUTER_API_KEY").unwrap())
        .build().unwrap();
    let provider = req.provider.clone().unwrap();
    match provider.as_str() {
        "kimi27code" => {
            let request = ChatCompletionBuilder::new("moonshotai/kimi-k2.7-code")
                .user_message(req.user_prompt.clone().unwrap())
                .temperature(req.temperature.unwrap_or(0.7))
                .max_tokens(req.max_tokens.unwrap_or(200.0) as u32)
                .top_p(req.top_p.unwrap_or(0.95))
                //todo freq penalty
                .system_message(req.system_prompt.clone().unwrap_or("".to_string()))
                .build();
            let response = client.chat_completion(request).await.unwrap();

            Ok(Json(AIResponse{
                output:response.choices[0].message.content.clone().unwrap()
            }))
        }
        "deepseekv4flash" => {
            let request = ChatCompletionBuilder::new("deepseek/deepseek-v4-flash")
                .user_message(req.user_prompt.clone().unwrap())
                .temperature(req.temperature.unwrap_or(0.7))
                .max_tokens(req.max_tokens.unwrap_or(200.0) as u32)
                .top_p(req.top_p.unwrap_or(0.95))
                //todo freq penalty
                .system_message(req.system_prompt.clone().unwrap_or("".to_string()))
                .build();
            let response = client.chat_completion(request).await.unwrap();
            print!("{:?}",response);
            Ok(Json(AIResponse{
                output:response.choices[0].message.content.clone().unwrap()
            }))
        }
        "groq" => {
            let api_key = std::env::var("GROQ_API_KEY").unwrap();
            let client = reqwest::Client::new();

            let response = client
                .post("https://api.groq.com/openai/v1/chat/completions")
                .header("Authorization", format!("Bearer {}", api_key))
                .json(&json!({
                    "model": "llama-3.1-8b-instant",
                    "temperature": req.temperature.unwrap_or(0.7),
                    "top_p": req.top_p.unwrap_or(0.95),
                    "max_tokens": req.max_tokens.unwrap_or(200.0) as u32,
                    "frequency_penalty": req.frequency_penalty.unwrap_or(0.0),
                    "messages": [{"role": "system", "content": req.system_prompt.clone().unwrap()},{"role": "user", "content": req.user_prompt.clone().unwrap()}],
                }))
                .send()
                .await.unwrap()
                .json::<serde_json::Value>()
                .await.unwrap();
            println!("{}", response);
            let out = response["choices"][0]["message"]["content"].as_str().unwrap().to_string();
            Ok(Json(AIResponse{
                output:out
            }))
        }

        _ => Err("missing provider".to_string()),
    }
}

pub struct CORS;

#[rocket::async_trait]
impl Fairing for CORS {
    fn info(&self) -> Info {
        Info {
            name: "Add CORS headers to responses",
            kind: Kind::Response
        }
    }

    async fn on_response<'r>(&self, _request: &'r Request<'_>, response: &mut Response<'r>) {
        response.set_header(Header::new("Access-Control-Allow-Origin", "http://localhost:3000")); //https://ai.esporterz.com
        response.set_header(Header::new("Access-Control-Allow-Methods", "POST, GET, PATCH, DELETE, OPTIONS"));
        response.set_header(Header::new("Access-Control-Allow-Headers", "*"));
        response.set_header(Header::new("Access-Control-Allow-Credentials", "true"));
    }
}

#[options("/<_..>")]
fn all_options() {
    /* Intentionally left empty */
}