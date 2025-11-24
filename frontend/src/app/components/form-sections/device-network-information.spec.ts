import { DeviceNetworkInformation } from '#components/form-sections';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('DeviceNetworkInformation', () => {
  let component: DeviceNetworkInformation;
  let fixture: ComponentFixture<DeviceNetworkInformation>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DeviceNetworkInformation],
    }).compileComponents();

    fixture = TestBed.createComponent(DeviceNetworkInformation);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
