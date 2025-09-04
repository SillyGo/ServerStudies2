#include <Arduino.h>
#include <WiFi.h>

const char* ssid = "***";
const char* senha = "***";
const char* host = "192.168.5.186";
const int port = 5050;

WiFiClient client; //o servidor já está configurado, aqui teremos só um cliente

void setup() //no setup, devemos nos conectar ao WiFi e ao servidor
{
  Serial.begin(115200);
  
  WiFi.begin(ssid, senha); //conecta
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(100);
    Serial.print(".");
  }
  Serial.println("\n Conexão WiFi estabelecida com sucesso!");

  if (!client.connect(host,port))
  {
    Serial.println("Conexão falhou ):");
    return;
  }
  Serial.println("Conectado ao Socket Server");

}

void loop()
{
  //nada acontece, por enquanto estou só testando a conexão com o socket server
}