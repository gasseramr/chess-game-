# 🎯 Enhanced Chess Game

A sophisticated Python-based chess game with an intelligent AI opponent, featuring an enhanced GUI and aggressive playing style.

![Chess Game](https://img.shields.io/badge/Python-3.12+-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.5.2-green)
![Python-Chess](https://img.shields.io/badge/Python--Chess-Latest-orange)

## 🚀 Features

### 🎮 **Game Features**
- **Three Difficulty Levels**: Easy, Medium, and Hard (Advanced AI)
- **Enhanced GUI**: Modern interface with gradient backgrounds and smooth animations
- **Game Controls**: New Game, Reset, Undo, and Settings buttons
- **Move History**: Real-time move tracking with SAN notation
- **Game Status Panel**: Shows current player, game status, and difficulty
- **Visual Highlights**: Selected pieces, valid moves, captures, and check indicators

### 🤖 **AI Intelligence**
- **Easy Mode**: Random moves for beginners
- **Medium Mode**: Basic strategic evaluation
- **Hard Mode**: Advanced AI with aggressive attacking style featuring:
  - **Aggressive Evaluation**: Enhanced piece-square tables for attacking play
  - **Tactical Awareness**: Detects mating opportunities and tactical combinations
  - **King Hunting**: Prioritizes moves that attack the enemy king
  - **Center Control**: Aggressive center occupation and piece development
  - **Anti-Repetition**: Prevents repetitive move patterns
  - **Opening Book**: Strong opening moves for early game advantage

### 🎨 **Visual Enhancements**
- **Gradient Backgrounds**: Beautiful visual effects
- **Piece Animations**: Smooth bounce animations for moves
- **Color-Coded Highlights**:
  - 🟡 Yellow: Selected piece
  - 🟢 Green: Valid moves
  - 🔴 Red: Captures and check
  - 🟠 Orange: Move indicators
- **Modern UI**: Clean, professional interface design

## 📋 Requirements

### **Python Dependencies**
```bash
pip install pygame
pip install python-chess
```

### **System Requirements**
- Python 3.12 or higher
- Windows 10/11 (tested)
- 4GB RAM minimum
- 100MB free disk space

## 🛠️ Installation

1. **Clone or Download** the project files
2. **Navigate** to the project directory:
   ```bash
   cd chess-game-
   ```
3. **Install Dependencies**:
   ```bash
   pip install pygame python-chess
   ```
4. **Run the Game**:
   ```bash
   python enhanced_chess.py
   ```

## 🎮 How to Play

### **Starting the Game**
1. Launch the game: `python enhanced_chess.py`
2. Press **'S'** to start from the welcome menu
3. Select difficulty level:
   - **1** - Easy (Random moves)
   - **2** - Medium (Basic strategy)
   - **3** - Hard (Advanced AI)

### **Game Controls**
- **Mouse Click**: Select and move pieces
- **New Game**: Start a fresh game
- **Reset**: Reset current game
- **Undo**: Take back the last move
- **Settings**: Change difficulty level

### **Game Rules**
- **White plays first** (you are White)
- **Black is the AI** opponent
- **Standard chess rules** apply
- **Pawn promotion** available (Q/R/B/N)
- **Check/Checkmate** detection
- **Stalemate** detection

## 🧠 AI Difficulty Levels

### **Easy Mode**
- **Strategy**: Random moves
- **Best for**: Beginners learning chess
- **Response Time**: Instant

### **Medium Mode**
- **Strategy**: Basic evaluation function
- **Features**: Piece value consideration, basic positioning
- **Best for**: Intermediate players
- **Response Time**: 0.5 seconds

### **Hard Mode (Advanced AI)**
- **Strategy**: Aggressive attacking play with tactical awareness
- **Features**:
  - Enhanced piece-square tables for aggressive positioning
  - King attack bonuses and tactical combinations
  - Opening book for strong early game
  - Anti-repetition logic to prevent loops
  - Weighted random selection from top moves
- **Best for**: Advanced players seeking challenge
- **Response Time**: 0.5 seconds

## 🎯 Advanced AI Features

### **Aggressive Playing Style**
The Hard mode AI is designed to be highly aggressive and attacking:

- **Increased Capture Bonuses**: Prioritizes capturing pieces
- **Enhanced Center Control**: Aggressive center occupation
- **King Attack Bonuses**: Rewards moves that attack the enemy king
- **Queen Activity**: Encourages early queen development
- **Pawn Advancement**: Aggressive pawn pushes
- **Tactical Detection**: Identifies mating opportunities

### **Technical Implementation**
- **Evaluation Function**: Multi-layered scoring system
- **Move Generation**: Legal move filtering with anti-repetition
- **Positional Understanding**: Piece-square tables for all pieces
- **Tactical Awareness**: Check detection and mate finding
- **Opening Book**: Pre-defined strong opening moves

## 📁 Project Structure

```
chess-game-/
├── enhanced_chess.py      # Main game file
├── test.py               # Original basic implementation
├── README.md             # This file
├── assets/               # Chess piece images
│   ├── white/           # White piece images
│   │   ├── wk.png       # White king
│   │   ├── wq.png       # White queen
│   │   ├── wr.png       # White rook
│   │   ├── wb.png       # White bishop
│   │   ├── wn.png       # White knight
│   │   └── wp.png       # White pawn
│   └── black/           # Black piece images
│       ├── bk.png       # Black king
│       ├── bq.png       # Black queen
│       ├── br.png       # Black rook
│       ├── bb.png       # Black bishop
│       ├── bn.png       # Black knight
│       └── bp.png       # Black pawn
└── Chess Documentation.* # Project documentation
```

## 🔧 Technical Details

### **Core Technologies**
- **Pygame**: Graphics and user interface
- **Python-Chess**: Chess logic and move validation
- **Python 3.12**: Programming language

### **Key Classes**
- **GameState**: Manages game state and history
- **Button**: Interactive UI buttons
- **AI Functions**: 
  - `evaluate_board()`: Position evaluation
  - `get_smart_ai_move()`: Advanced AI move selection
  - `get_opening_move()`: Opening book moves

### **Performance**
- **Frame Rate**: 60 FPS
- **AI Response**: 0.5 seconds
- **Memory Usage**: ~50MB
- **CPU Usage**: Low (single-threaded)

## 🐛 Troubleshooting

### **Common Issues**

**Game won't start:**
```bash
# Check Python version
python --version

# Install dependencies
pip install pygame python-chess

# Run with error output
python enhanced_chess.py 2>&1
```

**Missing piece images:**
- Ensure `assets/` folder contains all piece images
- Check file permissions

**Performance issues:**
- Close other applications
- Reduce system load
- Check available RAM

## 🎨 Customization

### **Modifying AI Behavior**
Edit `enhanced_chess.py`:
- **Line 443**: Modify `evaluate_board()` for different playing styles
- **Line 603**: Adjust `get_smart_ai_move()` for different strategies
- **Line 581**: Add new opening moves in `get_opening_move()`

### **Visual Customization**
- **Colors**: Modify constants at the top of the file
- **Fonts**: Change font settings in the constants section
- **Window Size**: Adjust `BOARD_SIZE` and `PANEL_WIDTH`

## 📈 Future Enhancements

### **Planned Features**
- [ ] **Sound Effects**: Move sounds and check alerts
- [ ] **Timer Functionality**: Game clocks and time controls
- [ ] **Save/Load Games**: Persistent game states
- [ ] **Network Play**: Online multiplayer
- [ ] **Analysis Mode**: Move analysis and suggestions
- [ ] **Custom Themes**: Multiple visual themes

### **AI Improvements**
- [ ] **Deep Learning**: Neural network integration
- [ ] **Opening Database**: Larger opening book
- [ ] **Endgame Tables**: Endgame optimization
- [ ] **Multi-threading**: Parallel move calculation

## 🤝 Contributing

### **How to Contribute**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### **Development Setup**
```bash
# Clone repository
git clone <repository-url>
cd chess-game-

# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Pygame Community**: For the excellent game development library
- **Python-Chess**: For robust chess logic implementation
- **Chess Community**: For inspiration and feedback

## 📞 Support

For issues, questions, or suggestions:
- Create an issue in the repository
- Contact the development team
- Check the documentation files

---

**Enjoy playing chess with the enhanced AI! 🎯♟️** 
