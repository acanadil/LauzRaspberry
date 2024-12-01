import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:toggle_switch/toggle_switch.dart';
import 'dart:async';

var urlVelocity = Uri.parse('http://pi1.local:5000/set_velocity');
var urlJobStart = Uri.parse('http://pi1.local:5000/start_job');
var urlJobEnd = Uri.parse('http://pi1.local:5000/end_job');
var urlProcStart = Uri.parse('http://pi1.local:5000/start_processing');
var urlProcEnd = Uri.parse('http://pi1.local:5000/stop_processing');

void main() {
  runApp(MainApp());
}

class MainApp extends StatefulWidget {
  @override
  State<MainApp> createState() => _MainAppState();
}

class _MainAppState extends State<MainApp> {
  bool isActiveJob = false;
  bool isActiveProc = false;
  bool viewProcess = false;
  bool viewJob = true;
  double sliderValue = 0;

  final List<String> _notifications = [];
  late Timer _timer;
  final String _apiUrl = 'http://pi1.local:5000/notifications';

  @override
  void initState() {
    super.initState();
    _startPolling();
  }

  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }

  void _startPolling() {
    _timer = Timer.periodic(const Duration(seconds: 5), (timer) async {
      await _fetchNotifications();
    });
  }

  Future<void> _fetchNotifications() async {
    try {
      final response = await http.get(Uri.parse(_apiUrl));

      if (response.statusCode == 200) {
        final List<dynamic> newNotifications = json.decode(response.body);

        setState(() {
          for (var notification in newNotifications) {
            if (!_notifications.contains(notification)) {
              _notifications.add(notification);
            }
          }
        });
      } else {
        print('Failed to fetch notifications: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching notifications: $e');
    }
  }

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
                SizedBox(
                  height: 40,
                ),
                Text(
                  'Velocity: ' + sliderValue.toStringAsFixed(1),
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
                Slider(
                  value: sliderValue,
                  max: 1,
                  min: -1,
                  divisions: 20,
                  label: sliderValue.toStringAsFixed(1),
                  onChanged: (double value) async {
                    var response = await http.post(urlVelocity,
                        headers: {
                          'Content-Type': 'application/json; charset=UTF-8'
                        },
                        body: json.encode({'velocity': value.toString()}));
                    print('Response status: ${response.statusCode}');
                    print('Response body: ${response.body}');
                    setState(() {
                      sliderValue = value;
                    });
                  },
                ),
                const SizedBox(height: 20), // Espaciado entre elementos
                ElevatedButton(
                  onPressed: () async {
                    setState(() {
                      sliderValue = 0;
                    });
                    var response = await http.post(urlVelocity,
                        headers: {
                          'Content-Type': 'application/json; charset=UTF-8'
                        },
                        body:
                            json.encode({'velocity': sliderValue.toString()}));
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.red,
                    padding: const EdgeInsets.symmetric(
                        horizontal: 24, vertical: 12),
                  ),
                  child: Text(
                    'Stop',
                    style: TextStyle(fontSize: 18, color: Colors.white),
                  ),
                ),

                if (viewJob)
                  Column(
                    children: [
                      SizedBox(height: 40),
                      Text(
                        'Job',
                        style: TextStyle(
                            fontSize: 20, fontWeight: FontWeight.bold),
                      ),
                      SizedBox(height: 10),
                      ToggleSwitch(
                        minWidth: 130.0,
                        activeBgColors: [
                          [Colors.red],
                          [Colors.green]
                        ],
                        activeFgColor: Colors.white,
                        inactiveBgColor: Color.fromARGB(133, 137, 137, 137),
                        inactiveFgColor: Colors.grey[900],
                        initialLabelIndex: isActiveJob ? 1 : 0,
                        totalSwitches: 2,
                        labels: ['Stop', 'Start'],
                        onToggle: (index) async {
                          if (index == 1) {
                            var response = await http.post(urlJobStart);
                            viewProcess = true;
                          } else {
                            var response = await http.post(urlJobEnd);
                            viewProcess = false;
                          }
                          setState(() {
                            isActiveJob = index == 1;
                          });
                        },
                      ),
                    ],
                  )
                else
                  SizedBox(height: 120),

                if (viewProcess)
                  Column(
                    children: [
                      SizedBox(height: 40),
                      Text(
                        'Process',
                        style: TextStyle(
                            fontSize: 20, fontWeight: FontWeight.bold),
                      ),
                      SizedBox(height: 10),
                      ToggleSwitch(
                        minWidth: 130.0,
                        activeBgColors: [
                          [Colors.red],
                          [Colors.green]
                        ],
                        activeFgColor: Colors.white,
                        inactiveBgColor: Color.fromARGB(133, 137, 137, 137),
                        inactiveFgColor: Colors.grey[900],
                        initialLabelIndex: isActiveProc ? 1 : 0,
                        totalSwitches: 2,
                        labels: ['Stop', 'Start'],
                        onToggle: (index) async {
                          if (index == 0) {
                            var response = await http.post(urlProcEnd);
                            viewJob = true;
                          } else {
                            var response = await http.post(urlProcStart);
                            viewJob = false;
                          }
                          setState(() {
                            isActiveProc = index == 1;
                          });
                        },
                      ),
                    ],
                  ),

                SizedBox(
                  height: 20,
                ),
                SizedBox(
                  height: 300,
                  child: ListView(
                    children: _notifications
                        .map((e) => ListTile(
                              title: Text(e),
                            ))
                        .toList(),
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
