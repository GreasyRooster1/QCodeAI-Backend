#[macro_use] extern crate rocket;



#[launch]
fn rocket() -> _ {
    rocket::build().mount("/", routes![
        status
    ])
}

#[get("/")]
fn status() -> &str {
    "running"
}