# Arbitrary Precision Printed Ternary Neural Networks with Holistic Evolutionary Approximation

This repository contains the implementation and experimental artifacts accompanying the paper:

**MRAZEK Vojtech, BALASKAS Konstantionos, DUARTE Carolina Lozano Paula, VAšíčEK Zdenek, TAHOORI Mehdi and ZERVAKIS Georgios.** *Arbitrary Precision Printed Ternary Neural Networks with Holistic Evolutionary Approximation.* IEEE Transactions on Circuits and Systems for Artificial Intelligence, 2025, pp. 13. ISSN 2996-6647.

```bibtex
@ARTICLE{FITPUB13265,
   author = "Vojtech Mrazek and Konstantionos Balaskas and Paula Lozano Carolina Duarte and Zdenek Vasicek and Mehdi Tahoori and Georgios Zervakis",
   title = "Arbitrary Precision Printed Ternary Neural Networks with Holistic Evolutionary Approximation",
   pages = "13",
   journal = "IEEE Transactions on Circuits and Systems for Artificial Intelligence",
   year = 2025,
   ISSN = "2996-6647",
}
```

## Abstract
Printed electronics offer a promising alternative for applications beyond silicon-based systems, requiring properties like flexibility, stretchability, conformality, and ultra-low fabrication costs. Despite the large feature sizes in printed electronics, printed neural networks have attracted attention for meeting target application requirements, though realizing complex circuits remains challenging. This work bridges the gap between classification accuracy and area efficiency in printed neural networks, covering the entire processing-near-sensor system design and co-optimization from the analog-to-digital interface--a major area and power bottleneck--to the digital classifier. We propose an automated framework for designing printed Ternary Neural Networks with arbitrary input precision, utilizing multi-objective optimization and holistic approximation. Our circuits outperform existing approximate printed neural networks by 17x in area and 59x in power on average, being the first to enable printed-battery-powered operation with under 5\% accuracy loss while accounting for analog-to-digital interfacing costs.

## Repository Structure

### 📁 [`TNN_moo/`](TNN_moo/)
Contains the core multi-objective optimization methodology and experimental setup:
- **Multiobjective optimization framework** using PyMoo library
- **Approximate component libraries** for Linear Threshold Gates (LTGs) and PopCount operations
- **Training and evaluation scripts** for the white wine quality dataset
- **Generated approximate circuits** optimized for area, power, and accuracy trade-offs
- **Pareto front visualization** tools and results

Key files:
- `whitewine3b.py`: Main TNN implementation and evaluation
- `moo_pcc_mb.py`: Multi-objective optimization script
- `AxLibrary/`: Complete library of exact and approximate LTG implementations

### 📁 [`Results/`](Results/)
Contains **Pareto-optimal TNN implementations** resulting from multi-objective optimization:
- `whitewine3b_exact/`: Reference exact implementation
- `whitewine3b_8102/`, `whitewine3b_9402/`, `whitewine3b_10727/`: Optimized approximate implementations
- Each folder contains synthesized circuits with area and power metrics
- All implementations target the white wine quality classification dataset

### 📄 [`generate_ltgs.py`](generate_ltgs.py)
**Arithmetic circuit generator** that creates tree adders and comparison operations:
- Utilizes the `arithsgen` module for CGP (Cartesian Genetic Programming) based approximation
- Generates multibit sum circuits and comparators
- Supports recursive tree structures for complex arithmetic operations
- Compatible with the approximate component optimization pipeline

### 📄 [`requirements.txt`](requirements.txt)
Python dependencies required for reproducing the experimental results.

## Getting Started

### Prerequisites
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### Running the Experiments
For detailed instructions and methodology, see the [TNN_moo/README.md](TNN_moo/README.md).

## License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

## Contact

For questions or issues regarding this implementation, please contact the authors or create an issue in this repository.
