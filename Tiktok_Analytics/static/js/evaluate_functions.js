([
    puzzlePiece,
    puzzlePieceOverlay,
    puzzleImageWrapper,]) => 
{
    const puzzlePieceEl = document.querySelector(puzzlePiece)
    const div = document.createElement('div')
    div.id = puzzlePieceOverlay.slice(1)

    const topPosition = Number(puzzlePieceEl.style.top.split('em')[0])
    Object.assign(div.style, {
      position: 'absolute',
      top: `${topPosition + 0.05}em`,
      left: puzzlePieceEl.style.left,
      width: '0.617536em',
      height: '0.617536em',
      backgroundColor: 'magenta',
    });

    puzzlePieceEl.style.display = 'none'
    document.querySelector(puzzleImageWrapper).appendChild(div)
  }


 _syncOverlayPositionWithPuzzlePiece([ puzzlePiece, puzzlePieceOverlay ])
  {
    const puzzlePieceEl = document.querySelector(puzzlePiece)
    const overlayEl = document.querySelector(puzzlePieceOverlay)
    overlayEl.style.left = puzzlePieceEl.style.left
  }

  _removeOverlayAndShowPuzzlePiece([ puzzlePieceOverlay, puzzlePiece ])
  {
   document.querySelector(puzzlePieceOverlay).remove()
   document.querySelector(puzzlePiece).style.display = 'block'
 }