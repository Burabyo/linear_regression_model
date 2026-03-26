import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Student Math Score Predictor',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        useMaterial3: true,
      ),
      home: const PredictionPage(),
    );
  }
}

class PredictionPage extends StatefulWidget {
  const PredictionPage({super.key});

  @override
  State<PredictionPage> createState() => _PredictionPageState();
}

class _PredictionPageState extends State<PredictionPage> {
  final _formKey = GlobalKey<FormState>();

  // API URL
  static const String apiUrl =
      'https://student-math-predictor-f5kr.onrender.com/predict';

  // Controllers for all 12 input fields
  final TextEditingController _genderCtrl = TextEditingController();
  final TextEditingController _parentEducCtrl = TextEditingController();
  final TextEditingController _lunchTypeCtrl = TextEditingController();
  final TextEditingController _testPrepCtrl = TextEditingController();
  final TextEditingController _parentMaritalCtrl = TextEditingController();
  final TextEditingController _practiceSportCtrl = TextEditingController();
  final TextEditingController _isFirstChildCtrl = TextEditingController();
  final TextEditingController _nrSiblingsCtrl = TextEditingController();
  final TextEditingController _transportCtrl = TextEditingController();
  final TextEditingController _studyHoursCtrl = TextEditingController();
  final TextEditingController _readingScoreCtrl = TextEditingController();
  final TextEditingController _writingScoreCtrl = TextEditingController();

  String _result = '';
  bool _isLoading = false;

  @override
  void dispose() {
    _genderCtrl.dispose();
    _parentEducCtrl.dispose();
    _lunchTypeCtrl.dispose();
    _testPrepCtrl.dispose();
    _parentMaritalCtrl.dispose();
    _practiceSportCtrl.dispose();
    _isFirstChildCtrl.dispose();
    _nrSiblingsCtrl.dispose();
    _transportCtrl.dispose();
    _studyHoursCtrl.dispose();
    _readingScoreCtrl.dispose();
    _writingScoreCtrl.dispose();
    super.dispose();
  }

  Future<void> _predict() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _isLoading = true;
      _result = '';
    });

    try {
      final response = await http.post(
        Uri.parse(apiUrl),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'Gender': int.parse(_genderCtrl.text),
          'ParentEduc': int.parse(_parentEducCtrl.text),
          'LunchType': int.parse(_lunchTypeCtrl.text),
          'TestPrep': int.parse(_testPrepCtrl.text),
          'ParentMaritalStatus': int.parse(_parentMaritalCtrl.text),
          'PracticeSport': int.parse(_practiceSportCtrl.text),
          'IsFirstChild': int.parse(_isFirstChildCtrl.text),
          'NrSiblings': int.parse(_nrSiblingsCtrl.text),
          'TransportMeans': int.parse(_transportCtrl.text),
          'WklyStudyHours': int.parse(_studyHoursCtrl.text),
          'ReadingScore': int.parse(_readingScoreCtrl.text),
          'WritingScore': int.parse(_writingScoreCtrl.text),
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          _result =
              'Predicted Math Score: ${data['predicted_math_score']}';
        });
      } else if (response.statusCode == 422) {
        setState(() {
          _result = 'Error: One or more values are out of range or invalid.';
        });
      } else {
        setState(() {
          _result = 'Error: ${response.statusCode} — ${response.body}';
        });
      }
    } catch (e) {
      setState(() {
        _result = 'Error: Could not connect to the API. $e';
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Widget _buildField({
    required String label,
    required String hint,
    required TextEditingController controller,
    required int min,
    required int max,
  }) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6.0),
      child: TextFormField(
        controller: controller,
        keyboardType: TextInputType.number,
        decoration: InputDecoration(
          labelText: label,
          hintText: hint,
          border: const OutlineInputBorder(),
          contentPadding:
              const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
        ),
        validator: (value) {
          if (value == null || value.isEmpty) {
            return '$label is required';
          }
          final parsed = int.tryParse(value);
          if (parsed == null) {
            return 'Enter a valid integer';
          }
          if (parsed < min || parsed > max) {
            return 'Value must be between $min and $max';
          }
          return null;
        },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Student Math Score Predictor'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // ── Info card ──────────────────────────────────────────────
              Card(
                color: Colors.indigo.shade50,
                child: const Padding(
                  padding: EdgeInsets.all(12.0),
                  child: Text(
                    'Enter student details below to predict their Math Score.\n'
                    'All values must be integers within the specified range.',
                    style: TextStyle(fontSize: 13, color: Colors.indigo),
                  ),
                ),
              ),
              const SizedBox(height: 12),

              // ── Input fields ───────────────────────────────────────────
              _buildField(
                label: 'Gender',
                hint: '0 = Female, 1 = Male',
                controller: _genderCtrl,
                min: 0,
                max: 1,
              ),
              _buildField(
                label: 'Parent Education Level',
                hint: '0 = Some high school ... 5 = Master\'s degree',
                controller: _parentEducCtrl,
                min: 0,
                max: 5,
              ),
              _buildField(
                label: 'Lunch Type',
                hint: '0 = Free/Reduced, 1 = Standard',
                controller: _lunchTypeCtrl,
                min: 0,
                max: 1,
              ),
              _buildField(
                label: 'Test Preparation',
                hint: '0 = Completed, 1 = None',
                controller: _testPrepCtrl,
                min: 0,
                max: 1,
              ),
              _buildField(
                label: 'Parent Marital Status',
                hint: '0 = Divorced, 1 = Married, 2 = Single, 3 = Widowed',
                controller: _parentMaritalCtrl,
                min: 0,
                max: 3,
              ),
              _buildField(
                label: 'Practice Sport',
                hint: '0 = Never, 1 = Sometimes, 2 = Regularly',
                controller: _practiceSportCtrl,
                min: 0,
                max: 2,
              ),
              _buildField(
                label: 'Is First Child',
                hint: '0 = No, 1 = Yes',
                controller: _isFirstChildCtrl,
                min: 0,
                max: 1,
              ),
              _buildField(
                label: 'Number of Siblings',
                hint: '0 to 7',
                controller: _nrSiblingsCtrl,
                min: 0,
                max: 7,
              ),
              _buildField(
                label: 'Transport Means',
                hint: '0 = Private, 1 = School Bus',
                controller: _transportCtrl,
                min: 0,
                max: 1,
              ),
              _buildField(
                label: 'Weekly Study Hours',
                hint: '0 = Less than 5, 1 = 5-10, 2 = More than 10',
                controller: _studyHoursCtrl,
                min: 0,
                max: 2,
              ),
              _buildField(
                label: 'Reading Score',
                hint: '0 to 100',
                controller: _readingScoreCtrl,
                min: 0,
                max: 100,
              ),
              _buildField(
                label: 'Writing Score',
                hint: '0 to 100',
                controller: _writingScoreCtrl,
                min: 0,
                max: 100,
              ),

              const SizedBox(height: 16),

              // ── Predict button ─────────────────────────────────────────
              ElevatedButton(
                onPressed: _isLoading ? null : _predict,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.indigo,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  textStyle: const TextStyle(
                      fontSize: 16, fontWeight: FontWeight.bold),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
                child: _isLoading
                    ? const SizedBox(
                        height: 20,
                        width: 20,
                        child: CircularProgressIndicator(
                          color: Colors.white,
                          strokeWidth: 2,
                        ),
                      )
                    : const Text('Predict'),
              ),

              const SizedBox(height: 20),

              // ── Result display ─────────────────────────────────────────
              if (_result.isNotEmpty)
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: _result.startsWith('Error')
                        ? Colors.red.shade50
                        : Colors.green.shade50,
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(
                      color: _result.startsWith('Error')
                          ? Colors.red
                          : Colors.green,
                    ),
                  ),
                  child: Text(
                    _result,
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: _result.startsWith('Error')
                          ? Colors.red.shade800
                          : Colors.green.shade800,
                    ),
                  ),
                ),

              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }
}