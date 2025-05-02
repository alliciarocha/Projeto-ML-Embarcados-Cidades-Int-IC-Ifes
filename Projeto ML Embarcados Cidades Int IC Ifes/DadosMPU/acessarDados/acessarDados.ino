#include <WiFi.h>
#include <LittleFS.h>
#include <ESPAsyncWebServer.h>

const char* ssid = "Allicia30";
const char* password = "123aaa123";

AsyncWebServer server(80);

void setup(){
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED){
    delay(1000);
    Serial.println("Conectando ao WiFi...");
  }
  Serial.println("WiFi conectado!");
  Serial.println(WiFi.localIP());

  if (!LittleFS.begin()) {
    Serial.println("Erro ao montar LittleFS");
    return;
  }

  // Listar arquivos no navegador
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    String fileList = "<h1>Arquivos no LittleFS:</h1><ul>";
    File root = LittleFS.open("/");
    File file = root.openNextFile();
    while(file){
      fileList += "<li><a href=\"/" + String(file.name()) + "\">" + String(file.name()) + "</a></li>";
      file = root.openNextFile();
    }
    fileList += "</ul>";
    request->send(200, "text/html", fileList);
  });

  // Servir arquivos
  server.onNotFound([](AsyncWebServerRequest *request){
    String path = request->url();
    if (LittleFS.exists(path)) {
      request->send(LittleFS, path, "text/plain");
    } else {
      request->send(404, "text/plain", "Arquivo não encontrado");
    }
  });

  server.begin();
}

void loop(){}
