import 'package:flutter/material.dart';

void main() {
  runApp(MainApp());
}

class MainApp extends StatefulWidget {
  @override
  State<MainApp> createState() => _MainAppState();
}

class _MainAppState extends State<MainApp> {
  int counter = 0; // Valor a modificar con los botones
  bool isActive = false; // Estado del botón rojo/verde

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Builder(
        builder: (BuildContext context) {
          return Scaffold(
            appBar: AppBar(
              title: Text('Lauzhack'),
              backgroundColor: const Color.fromARGB(255, 158, 187, 239),
            ),
            body: Column(
                mainAxisAlignment: MainAxisAlignment.start,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  SizedBox(height: 40,),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      ElevatedButton(
                        onPressed: () {
                          setState(() {
                            counter--;
                          });
                        },
                        child: Text('-'),
                      ),
                      Text(
                        '$counter',
                        style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                      ),
                      ElevatedButton(
                        onPressed: () {
                          setState(() {
                            counter++;
                          });
                        },
                        child: Text('+'),
                      ),
                    ],
                  ),
                  const SizedBox(height: 20), // Espaciado entre elementos
                  ElevatedButton(
                    onPressed: () {
                      setState(() {
                        isActive = !isActive; // Cambiar estado del botón
                      });
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: isActive
                          ?  Colors.red
                          : Colors.green, // Botón rojo si está desactivado
                      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                    ),
                    child: Text(
                      isActive ? 'Stop' : 'Activate',
                      style: TextStyle(fontSize: 18, color: Colors.white),
                    ),
                  ),
                ],
            ),
          );
        },
      ),
    );
  }
}