from cgitb import enable
import re
from PIL import Image
import imgcompare
 # backgroundColor: 'magenta',
class Captcha :
    options : any
    startImage = "start.jpeg"
    watchForCaptchaDomAdd =  """([verifyElement, verifyContainer]) =>
 {
     target = document.querySelector(verifyElement)

    if (document.querySelector(verifyContainer)) return Promise.resolve()

    return new Promise((resolve, reject) => {
       observer = new MutationObserver((mutations) => {
        for ( mutation of mutations) {
          if (mutation.addedNodes.length) {
            for ( addedNode of mutation.addedNodes) {
              if (
                addedNode.classList &&
                addedNode.classList.contains(verifyContainer.slice(1))
              ) {
                observer.disconnect()
                resolve()
                break
              }
            }
          }
        }
      })

      observer.observe(target, { childList: true, subtree: true })
    })
  }"""
    appendOverlayAndHidePuzzlePiece = """([puzzlePiece,puzzlePieceOverlay,puzzleImageWrapper]) =>
  {
    puzzlePieceEl = document.querySelector(puzzlePiece)
    div = document.createElement('div')
    div.id = puzzlePieceOverlay.slice(1)

    topPosition = Number(puzzlePieceEl.style.top.split('em')[0])
    Object.assign(div.style, {
      position: 'absolute',
      top: `${topPosition + 0.05}em`,
      left: puzzlePieceEl.style.left,
      width: '0.617536em',
      height: '0.617536em',
      opacity : '0.5',
      backgroundColor: 'black',
    })

    puzzlePieceEl.style.display = 'none' 
    document.querySelector(puzzleImageWrapper).appendChild(div)
    }"""
    _syncOverlayPositionWithPuzzlePiece = """([ puzzlePiece, puzzlePieceOverlay ]) =>
     {
    const puzzlePieceEl = document.querySelector(puzzlePiece)
    const overlayEl = document.querySelector(puzzlePieceOverlay)
    overlayEl.style.left = puzzlePieceEl.style.left
  }"""
    _removeOverlayAndShowPuzzlePiece = """([puzzlePieceOverlay, puzzlePiece ]) =>
 {
    document.querySelector(puzzlePieceOverlay).remove()
    document.querySelector(puzzlePiece).style.display = 'block'
  } """
    _waitForCaptchaDomRemove = """ async ([ verifyElement, verifyContainer ]) =>
 {
    return new Promise((resolve, reject) => {
      const observer = new MutationObserver((mutations) => {
        for (const mutation of mutations) {
          if (mutation.removedNodes.length) {
            for (const removedNode of mutation.removedNodes) {
              if (
                removedNode.classList &&
                removedNode.classList.contains(verifyContainer.slice(1))
              ) {
                observer.disconnect()
                resolve()
                break
              }
            }
          }
        }
      })
      observer.observe(document.querySelector(verifyElement), {
      childList: true,
      })

      setTimeout(reject.bind(this), 5000)
    })
  }"""
    disabeleScroll = """() => {
    // Get the current page scroll position
    scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    scrollLeft = window.pageXOffset || document.documentElement.scrollLeft,
  
        // if any scroll is attempted, set this to the previous value
        window.onscroll = function() {
            window.scrollTo(scrollLeft, scrollTop);
        };
}"""
    enableScroll = """() => {
    window.onscroll = function() {};
}"""
    
    def __init__(self) -> None:
        pass

    def isCaptchaUrl(url : str) -> bool:
        matchesSecurityCaptchaUrl = 'security-captcha' in url

        matchesByteImgUrls = re.search("captcha-\S{2,2}\.ibyteimg\.com\/\S+-2\.jpeg", url)

        return matchesSecurityCaptchaUrl or matchesByteImgUrls

    async def resize_img(img):
        readresult = Image.open(img)
        resize_img = readresult.resize((276,172))
        resize_img.save(img.split('.')[0] +".PNG")
        

    def get_defauls():
        return {
            "numAttempts": 3,
            "startPosition": 25,
            "positionIncrement": 5,
            }

    def get_selectors():
        return {
            "verifyElement": '[id$="verify-ele"], #login_slide',
            "verifyContainer": '.captcha_verify_container',
            "puzzleImageWrapper": '.captcha_verify_img--wrapper',
            "puzzleImage": '#captcha-verify-image',
            "puzzlePiece": '.captcha_verify_img_slide',
            "sliderElement": '.captcha_verify_slide--slidebar',
            "sliderHandle": '.secsdk-captcha-drag-icon',
            "puzzlePieceOverlay": '#captcha_overlay_box',
            }
    
