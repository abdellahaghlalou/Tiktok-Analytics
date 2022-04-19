from typing import Any
import re
from PIL import Image
#from promisio import promisify
import imgcompare
from playwright.sync_api import Playwright, sync_playwright

#diff = imgcompare.image_diff_percent()

class CaptchaSolver :
    page  : Any
    options : list
    startImage : Any
    watchForCaptchaDomAdd =  """_waitForCaptchaDomAdd([verifyElement, verifyContainer] ) {
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
    appendOverlayAndHidePuzzlePiece = """_appendOverlayAndHidePuzzlePiece([
    puzzlePiece,
    puzzlePieceOverlay,
    puzzleImageWrapper,
  ]) {
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
      backgroundColor: 'magenta',
    })

    puzzlePieceEl.style.display = 'none'
    document.querySelector(puzzleImageWrapper).appendChild(div)
  } """
    _syncOverlayPositionWithPuzzlePiece = """ _syncOverlayPositionWithPuzzlePiece([ puzzlePiece, puzzlePieceOverlay ]) {
    const puzzlePieceEl = document.querySelector(puzzlePiece)
    const overlayEl = document.querySelector(puzzlePieceOverlay)
    overlayEl.style.left = puzzlePieceEl.style.left
  }"""
    _removeOverlayAndShowPuzzlePiece = """_removeOverlayAndShowPuzzlePiece([puzzlePieceOverlay, puzzlePiece ]) {
    document.querySelector(puzzlePieceOverlay).remove()
    document.querySelector(puzzlePiece).style.display = 'block'
  } """
    _waitForCaptchaDomRemove = """ async _waitForCaptchaDomRemove([ verifyElement, verifyContainer ]) {
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
    

    def __init__(self, page): 
        self.page = page
        self.page.on('response', self._responseHandler )
  

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

    def solve(self) :
        if self.watchForCaptchaAdd :
          self.solve_until()
        else :
          print("no captcha found")

    def solve_until(self):
        CaptchaSolver.options = CaptchaSolver.get_defauls()
        isNotSolved = True

        while isNotSolved and CaptchaSolver.options["numAttempts"] > 0:
            isNotSolved = CaptchaSolver.solveCaptcha()
            CaptchaSolver.options["numAttempts"] -= 1

        return isNotSolved 

    def compare(img1,img2) -> int :
        return 0

    def captchaelts(self):
      return [
      self.get_selectors()["puzzleImageWrapper"],
      self.get_selectors()["puzzleImage"],
      self.get_selectors()["puzzlePiece"],
      self.get_selectors()["sliderElement"],
      self.get_selectors()["sliderHandle"],
    ]

    def watchForCaptchaAdd(self):
      try :
        self.page.wait_for_selector(CaptchaSolver.get_selectors()["verifyElement"], timeout=5000)
        self.page.evaluate(CaptchaSolver.watchForCaptchaDomAdd, CaptchaSolver.get_selectors())

        for el in self.captchaelts() :
          self.page.waitForSelector(el, { 'state': 'attached' })
        return True
      except :  
        return False
      
    def solveCaptcha(self):
      self.page.evaluate(CaptchaSolver.appendOverlayAndHidePuzzlePiece,
                         [CaptchaSolver.get_selectors()["puzzlePiece"],
                          CaptchaSolver.get_selectors()["puzzlePieceOverlay"],
                          CaptchaSolver.get_selectors()["puzzleImageWrapper"]])

      sliderElement =  self.page.query_selector(CaptchaSolver.get_selectors().sliderElement)
      sliderHandle =  self.page.query_selector(CaptchaSolver.get_selectors().sliderHandle)
      slider =  sliderElement.bounding_box()
      handle =  sliderHandle.bounding_box()

      currentPosition = self.options.startPosition

      target = {
      "position": 0,
      "difference": 100,
    }

      self.page.waitForTimeout(3000)
      self.page.mouse.move(
      handle.x + handle.width / 2,
      handle.y + handle.height / 2
    )
      self.page.mouse.down()

      while   currentPosition < slider.width - handle.width / 2 :
        self.page.mouse.move(
        handle.x + currentPosition,
        handle.y + handle.height / 2)
      

        self.page.evaluate(
        CaptchaSolver._syncOverlayPositionWithPuzzlePiece,
        [CaptchaSolver.get_selectors()["puzzlePiece"],
        CaptchaSolver.get_selectors()["puzzlePieceOverlay"]])
      

        sliderContainer =  self.page.query_selector(
        CaptchaSolver.get_selectors["puzzleImageWrapper"]
      )

        sliderImage =  self.page.screenshot({
        "clip":  sliderContainer.bounding_box(),
      })

        
        curr = Image.open(sliderImage)
        curr = curr.resize((276, 172))
        curr.save("current.png")

      #  rembrandt = new Rembrandt({
      #   imageA: self.startImage,
      #   imageB: currentImage,
      #   thresholdType: Rembrandt.THRESHOLD_PIXELS,
      # })

        difference = imgcompare.image_diff_percent("current.png", "start.png")

        if target.difference > difference :

          target.difference = difference
          target.position = currentPosition
      

        currentPosition += self.options.positionIncrement
    

      self.page.evaluate(
      CaptchaSolver._removeOverlayAndShowPuzzlePiece,
      [CaptchaSolver.get_selectors()["puzzlePieceOverlay"],
      CaptchaSolver.get_selectors()["puzzlePiece"]]
    )
      isVerifyPage =  self._isVerifyPage()

      self.page.mouse.move(
      handle.x + target.position,
      handle.y + handle.height / 2
    )
      self.page.mouse.up()

      return self._waitForCaptchaDismiss(isVerifyPage)

    def _isVerifyPage(self):
      self.page.title() == 'tiktok-verify-page'

    def _waitForCaptchaDismiss(self, isVerifyPage):
      if isVerifyPage :
        try :
          waitstr =  "networkidle" if True else "networkidle0"
          self.page.expect_navigation(timeout= 5000,waitUntil = "networkidle0")
        except :
          print("timeout")
        return self._isVerifyPage()
      
      try :
        return  self.page.evaluate(
        CaptchaSolver._waitForCaptchaDomRemove,
        [CaptchaSolver.get_selectors()["verifyElement"],
        CaptchaSolver.get_selevtors()["verifyContainer"]]
      )
      except :
        return True

    def isPlaywright(self) :
      pass

    def _responseHandler(self,response):
      maxContentLength = -1
      print(response)
      responseUrl = response.url()
      if not self.validCaptchaUrl(responseUrl):
        return
      contentLength = int(response.headers()['content-length'])
      if contentLength > maxContentLength:
        maxContentLength = contentLength
        CaptchaSolver.startImage = self.resize_img(response.body())

    def validCaptchaUrl(self, url) :
      matchesSecurityCaptchaUrl = 'security-captcha' in url

      matchesByteImgUrls = re.search("/captcha-\S{2,2}\.ibyteimg\.com\/\S+-2\.jpeg/", url)

      return matchesSecurityCaptchaUrl or matchesByteImgUrls
    
    def resize_img(self,img):
      readresult = Image.open(img)
      resize_img = readresult.resize((276,172))
      resize_img.save("start.png")
      return "start.png"