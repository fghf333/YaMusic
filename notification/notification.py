import objc

NSUserNotification = objc.lookUpClass("NSUserNotification")
NSUserNotificationCenter = objc.lookUpClass("NSUserNotificationCenter")
NSObject = objc.lookUpClass("NSObject")


class NotificationDelegator(NSObject):

    def userNotificationCenter_didActivateNotification_(self, center, notification):
        print("Activate notification")

    def userNotificationCenter_shouldPresentNotification_(self, center, notification):
        print("Should present notification")
        return True


delegator = NotificationDelegator.alloc().init()


def notify(title="", subtitle="", info_text="", delay=1, sound=False, userInfo={}):
    """ Python method to show a desktop notification on Mountain Lion. Where:
        title: Title of notification
        subtitle: Subtitle of notification
        info_text: Informative text of notification
        delay: Delay (in seconds) before showing the notification
        sound: Play the default notification sound
        userInfo: a dictionary that can be used to handle clicks in your
                  app"s applicationDidFinishLaunching:aNotification method
    """
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(title)
    notification.setSubtitle_(subtitle)
    notification.setInformativeText_(info_text)
    notification.setUserInfo_(userInfo)
    if sound:
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
    center = NSUserNotificationCenter.defaultUserNotificationCenter()
    center.setDelegate_(delegator)
    center.deliverNotification_(notification)
