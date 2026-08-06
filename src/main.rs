#[macro_use] extern crate rocket;

use std::env;
use std::sync::Arc;
use openrouter_rust::OpenRouterClient;
use rocket::fairing::{Fairing, Info, Kind};
use rocket::{Request, Response};
use rocket::http::Header;
use rocket::serde::json::Json;
use rocket::serde::{Deserialize, Serialize};
use rocket_firebase_auth::{FirebaseAuth, FirebaseToken};

struct ServerState {
    auth: FirebaseAuth,
}

#[derive(Serialize,Deserialize)]
struct AIResponse{
    output:String,
}
#[derive(Serialize,Deserialize)]
struct AIRequest {
    provider: String,
    system_prompt: String,
    user_prompt: String,
    temperature: f32,
    top_p: f32,
    frequency_penalty: f32,
    max_tokens: f32,
}

#[launch]
async fn rocket() -> _ {

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
fn generate(token: FirebaseToken,req: Json<AIRequest>) -> Result<Json<AIResponse>, String> {
    let client = OpenRouterClient::builder()
        .api_key(env::var("OPENROUTER_API_KEY"))
        .build()?;
    match req.provider.as_str() {
        "kimi27code" => {
            Ok(Json(AIResponse {
                output: req.user_prompt.clone(),
            }))
        }
        "deepseekv4flash" => {
            Ok(Json(AIResponse {
                output: req.user_prompt.clone(),
            }))
        }
        "groq" => {
            Ok(Json(AIResponse {
                output: req.user_prompt.clone(),
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
        response.set_header(Header::new("Access-Control-Allow-Origin", "http://localhost:3000"));
        response.set_header(Header::new("Access-Control-Allow-Methods", "POST, GET, PATCH, DELETE, OPTIONS"));
        response.set_header(Header::new("Access-Control-Allow-Headers", "*"));
        response.set_header(Header::new("Access-Control-Allow-Credentials", "true"));
    }
}

#[options("/<_..>")]
fn all_options() {
    /* Intentionally left empty */
}