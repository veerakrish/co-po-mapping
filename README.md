# CO-PO Mapping Matrix Generator

A web application to automatically generate Course Outcomes (CO) to Program Outcomes (PO) and Program Specific Outcomes (PSO) mapping matrix using semantic analysis.

## Features

- Upload CO text file and automatically generate mapping matrix
- Semantic matching algorithm to determine mapping strength
- Support for knowledge levels (K1-K6)
- Generates mapping on a scale of 1-3
- Calculates average attainment for each PO/PSO
- Export results as CSV file
- Clean and intuitive web interface

## Installation & Usage

### Method 1: Using Python (Development)

1. Clone the repository:
   ```bash
   git clone https://github.com/veerakrish/co-po-mapping.git
   cd co-po-mapping
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the web application:
   ```bash
   python app.py
   ```

5. Open your browser and go to: http://localhost:5000

### Method 2: Using Docker

1. Install Docker on your system

2. Build and run the container:
   ```bash
   docker build -t co-po-mapping .
   docker run -p 5000:5000 co-po-mapping
   ```

3. Open your browser and go to: http://localhost:5000

### Method 3: Standalone Executable (Windows)

1. Download the latest release from the GitHub releases page
2. Extract the zip file
3. Double-click `start_webapp.bat`
4. The application will automatically open in your default browser

## Input File Format

Create a text file with your Course Outcomes (COs) in the following format:

```
CO1: Apply Divide and Conquer algorithm technique to solve complex problems in logarithmic time. [K3]
CO2: Apply Greedy method to solve Optimization problems. [K3]
CO3: Design and implement Dynamic Programming solutions. [K4]
```

Each CO should:
- Start with "CO" followed by a number
- Include a description
- End with a knowledge level in square brackets [K1] to [K6]

## Output

The application generates:
1. An interactive web-based mapping matrix
2. A downloadable CSV file with the mapping matrix
3. Average attainment levels for each PO/PSO

## How the Mapping Works

The application uses a semantic matching algorithm that:
1. Analyzes keywords in COs and POs/PSOs
2. Considers knowledge levels (K1-K6)
3. Assigns mapping strength:
   - 3: Strong correlation
   - 2: Medium correlation
   - 1: Low correlation
   - Empty: No correlation

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Flask, NumPy, and Pandas
- Uses Bootstrap for the user interface
- Semantic matching algorithm inspired by NLP techniques

## Support

For support, please open an issue in the GitHub repository: https://github.com/veerakrish/co-po-mapping/issues
