#ifndef RESEAU_ZEUS_H
#define RESEAU_ZEUS_H

#include <Arduino.h>
#include <WiFi.h>
#include <esp_now.h>
#include "ZeusData.h"

class ReseauZeus {
  public:
    // Définition du type de fonction que le main devra fournir
    typedef void (*UserCallback)(struct_data data);

  private:
    UserCallback _userCallback;
    static ReseauZeus* _instance; // CORRECTION 1: Type mis à jour (ReseauZeus)

    // CORRECTION 2 : Nouvelle signature pour ESP32 Core 3.0+
    // Avant : (const uint8_t * mac, ...)
    // Maintenant : (const esp_now_recv_info_t * info, ...)
    static void OnDataRecv(const esp_now_recv_info_t * info, const uint8_t *incomingData, int len) {
        if (_instance && _instance->_userCallback) {
            struct_data data;
            // Vérification de sécurité de la taille
            if (len == sizeof(data)) {
                memcpy(&data, incomingData, sizeof(data));
                _instance->_userCallback(data);
            }
        }
    }

    // CORRECTION 3 : Nouvelle signature Send pour ESP32 Core 3.0+
    static void OnDataSent(const wifi_tx_info_t *info, esp_now_send_status_t status) {
        // Optionnel : Debug
        // Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Envoi OK" : "Echec Envoi");
    }

  public:
    // CORRECTION 1: Le constructeur doit avoir le même nom que la classe
    ReseauZeus() {
        _instance = this; 
    }

    void begin(UserCallback callback) {
        _userCallback = callback;

        WiFi.mode(WIFI_STA);
        
        // Initialisation ESP-NOW
        if (esp_now_init() != ESP_OK) {
            Serial.println("Erreur Init ESP-NOW");
            return;
        }

        // Enregistrement des callbacks
        esp_now_register_recv_cb(OnDataRecv);
        esp_now_register_send_cb(OnDataSent);
        
        Serial.println("Réseau Zeus Initialisé");
    }

    void ajouterPair(const uint8_t* macAddr) {
        esp_now_peer_info_t peerInfo = {};
        memcpy(peerInfo.peer_addr, macAddr, 6);
        peerInfo.channel = 0;  
        peerInfo.encrypt = false;
        
        if (esp_now_add_peer(&peerInfo) != ESP_OK) {
            Serial.println("Erreur ajout pair");
        }
    }

    void envoyerBroadcast(struct_data data) {
        // NULL envoie à tous les pairs enregistrés
        esp_now_send(NULL, (uint8_t *) &data, sizeof(data));
    }
};

// Initialisation du pointeur statique (avec le bon type)
ReseauZeus* ReseauZeus::_instance = nullptr;

#endif